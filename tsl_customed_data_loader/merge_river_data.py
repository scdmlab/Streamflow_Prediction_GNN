import pandas as pd
import os
from glob import glob

# Data directory
data_dir = "data_time_series"

# Get all CSV files
csv_files = glob(os.path.join(data_dir, "*_data.csv"))

# Store data from all stations
dataframes = []

for file in csv_files:
    # Extract station ID, e.g., "519_data.csv" → "519"
    station_id = os.path.basename(file).split("_")[0]
    
    # Read CSV, keeping only datetime and discharge columns
    df = pd.read_csv(file, usecols=["datetime", "discharge"])
    
    # Replace / with - in date format to unify the format
    df["datetime"] = df["datetime"].str.replace("/", "-")
    
    # Convert datetime column to pandas datetime object
    df["datetime"] = pd.to_datetime(df["datetime"], format="%Y-%m-%d %H:%M:%S", errors="coerce")  # Return NaT on error
    
    # Check for NaT values
    if df["datetime"].isnull().any():
        print(f"Warning: There are missing datetime values in {station_id}")
    
    # Remove duplicate timestamps, keeping the first occurrence
    df = df.drop_duplicates(subset=["datetime"])
    
    # Set datetime as index
    df.set_index("datetime", inplace=True)

    # Rename discharge column to station_id
    df.rename(columns={"discharge": station_id}, inplace=True)

    # Store in list
    dataframes.append(df)

# Merge data from all stations by time index
df_final = pd.concat(dataframes, axis=1, join="outer")  # "outer" keeps all time points
df_final.sort_index(inplace=True)  # Ensure chronological order

# Fill missing values (if some stations do not have data for specific times)
df_final = df_final.interpolate()  # Linear interpolation
df_final.ffill(inplace=True)  # Forward fill
df_final.bfill(inplace=True)  # Backward fill

# Print the first few rows
print(df_final.head())
# Drop the last row
df_final = df_final.drop(df_final.tail(1).index)

# Save the merged data
df_final.to_csv("merged_discharge_data.csv")