import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

import numpy as np

def STAGE1(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')

    # Get unique vessel names
    vessel_names = df['VESSEL'].unique()

    # Create separate sheets for each vessel
    with pd.ExcelWriter('split_data.xlsx') as writer:
        for vessel_name in vessel_names:
            vessel_data = df[df['VESSEL'] == vessel_name]
            vessel_data.to_excel(writer, sheet_name=vessel_name, index=False)

def STAGE2(file_path):
    xl = pd.ExcelFile(file_path)

    # Create a Pandas Excel writer object
    output_file = 'clustered_output_file_final.xlsx'  # Replace with your desired output file path
    writer = pd.ExcelWriter(output_file, engine='openpyxl')

    # Process each sheet in the Excel file
    for sheet_name in xl.sheet_names:
        # Read data from the current sheet
        df = xl.parse(sheet_name)

        # Extract 'POD' column data
        pod_data = df['POD']

        # Perform TF-IDF vectorization on the 'POD' data
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(pod_data)

        # Perform KMeans clustering
        n_clusters = 5  # Number of clusters, adjust as needed
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        kmeans.fit(X)

        # Add 'Cluster' column to the DataFrame
        df['Cluster'] = kmeans.labels_

        # Write the modified DataFrame to a new sheet in the Excel file
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Save the Excel file with clustered data
    writer._save()

def STAGE3(file_path):
    xl = pd.ExcelFile(file_path)

    # Create a Pandas Excel writer object for sorted, modified, and re-sorted data
    re_sorted_output_file = 'weight_classification_cluster_file.xlsx'  # Replace with desired re-sorted output file path
    re_sorted_writer = pd.ExcelWriter(re_sorted_output_file, engine='openpyxl')

    # Process each sheet in the Excel file
    for sheet_name in xl.sheet_names:
        # Read data from the current sheet
        df = xl.parse(sheet_name)

        # Sort data within each cluster using rule-based heuristic
        df['Sorting_Rank'] = df['TEU'] * 1000 + df['WEIGHT']  # Assuming higher TEU is more important
        df = df.sort_values(by=['Cluster', 'Sorting_Rank'], ascending=[True, False])
        df = df.drop(columns=['Sorting_Rank'])

        # Define the conditions for different TEU classes
        conditions = [
            (df['TEU'] == 1),
            (df['TEU'] == 2)

        ]

        # Define the corresponding class names
        class_names = ['TEU 1 Group', 'TEU 2 Group']
        # Add names for other TEU values

        # Add 'Group' column based on TEU ranges within each cluster
        df['Group'] = pd.Categorical.from_codes(
            np.select(conditions, range(len(conditions)), default=-1),
            categories=class_names
        )

        conditions2 = [
            (df['WEIGHT'] >= 2) & (df['WEIGHT'] <= 11.9),
            (df['WEIGHT'] >= 12) & (df['WEIGHT'] <= 17.9),
            (df['WEIGHT'] >= 18) & (df['WEIGHT'] <= 23.9),
            (df['WEIGHT'] >= 24)
        ]

        class_names = ['Class 1', 'Class 2', 'Class 3', 'Class 4']
        df['Class'] = pd.Categorical.from_codes(
            np.select(conditions2, range(len(conditions2)), default=-1),
            categories=class_names
        )
        # Write the sorted, modified, and re-sorted DataFrame to a new sheet in the re-sorted Excel file
        df.to_excel(re_sorted_writer, sheet_name=sheet_name, index=False)

    # Save the re-sorted Excel file
    re_sorted_writer._save()

def find_available_bay(occupied_bays, current_bay, total_bay):
    # Find the next available bay that is not already occupied
    for bay in range(current_bay, total_bay + 1):
        if bay not in occupied_bays:
            return bay

    # Wrap around the bay count if all bays are occupied
    return 1

def STAGE4(file_path):
    xl = pd.ExcelFile(file_path)

    # Create a Pandas Excel writer object for the final arrangement
    final_output_file = 'final_container_arrangement_updated.xlsx'  # Replace with desired output file path
    final_writer = pd.ExcelWriter(final_output_file, engine='openpyxl')

    # Constants for slot and cluster calculations
    total_slots_per_bay = 28
    max_containers_per_slot = 30
    total_bay = 13

    # Initialize variables for bay assignment and ship tracking
    bay_assignment = {}  # Stores the bay assignment for each ship
    current_bay = 1
    occupied_bays = set()

    for sheet_name in xl.sheet_names:
        # Read data from the current sheet (ship)
        df = xl.parse(sheet_name)

        # Sort ship data by arrival date
        df['ARRIVAL'] = pd.to_datetime(df['ARRIVAL DATE'])
        df = df.sort_values(by='ARRIVAL')

        # Sort data within each cluster using rule-based heuristic (if needed)
        df = df.sort_values(by=['Cluster', 'TEU'], ascending=[True, True])

        # Check if the current ship has the same arrival date as the previous one
        arrival_date = df['ARRIVAL'].iloc[0]

        if arrival_date in bay_assignment:
            # Assign the same bay as the previous ship with the same arrival date
            current_bay = bay_assignment[arrival_date]
        else:
            # Assign a new bay if the arrival date is different
            current_bay = find_available_bay(occupied_bays, current_bay, total_bay)
            bay_assignment[arrival_date] = current_bay
            occupied_bays.add(current_bay)

        # Initialize variables for slot and cluster tracking for the current ship
        current_slot = 1
        container_count = 0
        last_TEU = 1

        for index, row in df.iterrows():
            container_TEU = row['TEU']
            last_cluster = row['Cluster']

            if last_TEU != container_TEU or last_cluster != row['Cluster']:
                current_slot += 2  # Move to the next-to-next slot for a new cluster
                container_count = 0  # Reset container count for the new slot

                if current_slot > total_slots_per_bay:
                    current_slot -= total_slots_per_bay  # Wrap around the slot count
                    current_bay = find_available_bay(occupied_bays, current_bay, total_bay)
                    occupied_bays.add(current_bay)

            # Assign slots based on container TEU
            df.at[index, 'Bay'] = current_bay
            df.at[index, 'Slot'] = current_slot

            # Update container count for the slot
            container_count += container_TEU
            last_TEU = container_TEU

        # Write the allocation to the final Excel file
        df.to_excel(final_writer, sheet_name=sheet_name, index=False)

    # Save the final arrangement Excel file
    final_writer._save()

    print("Ship-to-Bay Mapping:", bay_assignment)

STAGE1('MainCode\shipdataset_EXPORT.xlsx')
STAGE2('split_data.xlsx')
STAGE3('clustered_output_file_final.xlsx')
STAGE4('weight_classification_cluster_file.xlsx')