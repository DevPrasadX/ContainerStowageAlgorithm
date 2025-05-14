PAPER TITLE
An integrated rule based heuristic approach for optimization of container stowage on seaport terminals using machine learning 
PRASAD PANSARE, PRASAD PANDE, NISHANT PANDEY, ANMOL SINGH DADIAL
TOLANI MARITIME INSTITUTE , PUNE
MIT WORLD PEACE UNIVERSITY , PUNE
--------------------------------------------------------------------------------------------------------------------
One of the most pressing issues in the  maritime sector revolves around the efficient relocation of containerized cargo within seaport terminals. Even minor adjustments in cargo processing procedures can yield remarkable outcomes, 
including substantial cost savings and a noteworthy reduction in carbon emissions. This Project aims at providing an optimized container stowage plan using machine learning and “rule-based heuristic algorithm”, considering factors like
the intended port of discharge, weight of containers, space available on the terminal, the desired transfer rate of containers, and the type of container in use.
To aid our research we visited the PSA BMCT terminal where we had a first hand glimpse on port operations and got an insight on the current scenario regarding handling of containers.
We did an in-depth study of the method of clusterization and the softwares used along with their limitations
-------------------------------------------------------------------------------------------------------------------
ROADBLOCKS:
Practical constraints pertaining to stowage of containers on sea port terminals include:

Sudden change in the arrival time of containers on port
Change in berthing schedule of vessels
Concentrated movements of ITVs on the terminal leading to traffic
Improper allocation of RTGs due to improper stowage plan leading to increased ideal time
Change in port of discharge of vessels
-------------------------------------------------------------------------------------------------------------------

As a result, this effects the performance of many factors , such as :
Inefficient utilization of ITV’s , QC’s and RTG’s
Internal traffic of ITVs in ports
Increasing the docking period of the respective vessels 
It’s recurring consequences are economic loss and environmental impact

IMPLEMENTING HEURISTIC ALGORITHM AND MACHINE LEARNING
Heuristic algorithms optimize bay assignment and container placement, enhancing resource use and potentially reducing operational costs.
The implemented heuristic algorithms optimize container arrangement in shipping by efficiently assigning bays based on ship arrival dates and strategically placing containers within each bay according to their TEU sizes and clusters
ML groups similar 'POD' values using a text analysis tool and clustering technique.

-------------------------------------------------------------------------------------------------------------------
WORKING
STAGE1: 
Segregation of Data. The program begins by taking an Excel file (’shipdatasetEXPORT.xlsx’) containing data on multiple ships and their respective container details. It reads this data and creates separate Excel 
sheets for each vessel, segregating the data based on the ’VESSEL’ column. 
• STAGE2: 
Clustering of POD (Port of Discharge) It takes the segregated Excel file (’splitdata.xlsx’) created in STAGE1 and reads each sheet (ship data). Utilizes TF-IDF vectorization on the ’POD’ (Port of Discharge) data 
and performs KMeans clustering on it. Adds a ’Cluster’ column to each ship’s data based on the clustering results and saves this updated information into a new Excel file. 
• STAGE3:
Classification and Sorting by TEU and Weight Reads the clustered output file (’clusteredoutputf ilef inal.xlsx’) generated from STAGE2. Sorts data within each cluster based on a rule based heuristic, considering 
’TEU’ (Twenty-foot Equivalent Unit) and ’WEIGHT’ columns. Divides the data into different groups/classes (’Group’ and ’Class’ columns) based on specified conditions. Saves the modified data into a new Excel file with sorted and 
classified information. 
• STAGE4:   Bays and Allocation Slots Reads of (’weightclassificationclusterfile.xlsx’) Containers The modified to file generated from STAGE3. Arranges containers from different ships into bays and slots based on several conditions 
including ’TEU’, ’Cluster’, and ’ARRIVAL DATE’. Allocates bays and slots to containers in a way that optimizes the available space. Generates a final Excel file (’finalcontainerarrangementupdated.xlsx’) with 
the allocation details. The program’s execution begins by receiving input data regarding ships and containers, then systematically processes and manipulates this data through the aforementioned stages, ultimately producing 
a final allocation arrangement of containers into bays and slots for efficient management and handling at the port. 
