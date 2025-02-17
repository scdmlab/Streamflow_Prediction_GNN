import pandas as pd
import numpy as np
from tsl.data import SpatioTemporalDataset
from tsl.data.preprocessing import StandardScaler

# Assume you have already loaded the discharge data (merged_discharge_data.csv) and adjacency matrix (adj_matrix.csv)
# Load discharge data
def load_data(file_path):
    return pd.read_csv(file_path, parse_dates=["datetime"], index_col="datetime")

# Load adjacency matrix
def load_adjacency_matrix(file_path):
    return np.genfromtxt(file_path, delimiter=",")  # Assume the adjacency matrix is in CSV format

# Load data
discharge_data_path = "merged_discharge_data.csv"
adjacency_matrix_path = "adj_matrix.csv"

df_discharge = pd.read_csv(discharge_data_path, parse_dates=["datetime"])
adjacency_matrix = load_adjacency_matrix(adjacency_matrix_path)

# Extract time series data (excluding the datetime column, assuming each column is the discharge data for a station)
data = df_discharge.drop(columns=["datetime"]).values

# Data normalization
scaler = StandardScaler()  # Data normalization
data_normalized = scaler.fit_transform(data)  # Normalize data

# Create SpatioTemporalDataset
window_size = 24  # Use the past 24 time steps
horizon = 12  # Predict the next 12 time steps

dataset = SpatioTemporalDataset(
    target=data_normalized,            # Your normalized time series data
    connectivity=adjacency_matrix,     # Sensor connectivity (adjacency matrix)
    mask=None,                         # Whether there are missing values, if so, you can pass a mask
    horizon=horizon,                   # Predict the next 12 time steps
    window=window_size,                # Use the past 24 time steps as input
    transform=scaler                   # Normalization
)

# Output basic information about the dataset
print(f"Dataset length: {len(dataset)}")