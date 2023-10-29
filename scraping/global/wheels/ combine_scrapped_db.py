import glob
import pandas as pd
import os
import re  # Import the regular expression module

# Get a list of all csv files in the directory that match the pattern "wheels_*.csv"
csv_files = glob.glob("/Users/marko/data_science/cycling_marketplace/scraping/global/wheels/data/wheels_*.csv")

# Create an empty list to store the dataframes
dfs = []

# Loop through each csv file
for file in csv_files:
    # Read the csv file into a dataframe
    df = pd.read_csv(file)
    
    # Use the re module to extract the part of the file name between "wheels_" and ".csv"
    # Alternatively, you could use string methods to achieve the same result
    store_name = re.search(r'wheels_(.*).csv', os.path.basename(file)).group(1)
    
    # Create a new column 'store' and set its value to the extracted substring
    df['store'] = store_name
    
    # Append the dataframe to the list of dataframes
    dfs.append(df)

# Concatenate all dataframes in the list into a single dataframe
combined_df = pd.concat(dfs)

# Write the combined dataframe to a new csv file
combined_df.to_csv("/Users/marko/data_science/cycling_marketplace/scraping/global/wheels/data/combined_wheels.csv", index=False)
