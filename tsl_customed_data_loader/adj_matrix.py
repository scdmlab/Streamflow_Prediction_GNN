import pandas as pd
import numpy as np

# Load discharge data to get station IDs
discharge_data_path = "merged_discharge_data.csv"
df_discharge = pd.read_csv(discharge_data_path)

# Get station IDs from the first row (excluding the first column 'datetime')
station_ids = df_discharge.columns[1:]
num_stations = len(station_ids)

# Create a mapping from station_id to index
station_to_index = {station: i for i, station in enumerate(station_ids)}

# Initialize the adjacency matrix
adj_matrix = np.zeros((num_stations, num_stations))

# Read the catchment relationship table
catchment_relationship_path = "catchment_relationship.csv"
df_relationship = pd.read_csv(catchment_relationship_path)

# Fill the adjacency matrix
for _, row in df_relationship.iterrows():
    downstream = row["station_id"]
    upstream = row["upstream_id"]

    if upstream in station_to_index and downstream in station_to_index:
        i, j = station_to_index[upstream], station_to_index[downstream]
        adj_matrix[i, j] = 1  # Upstream flows to downstream (unidirectional)

# Save the adjacency matrix to a CSV file
adj_matrix_path = "adj_matrix.csv"
np.savetxt(adj_matrix_path, adj_matrix, delimiter=",")

print("Adjacency matrix has been saved to adj_matrix.csv.")