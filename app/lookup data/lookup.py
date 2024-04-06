import os
import pandas as pd

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the filename of the CSV file
file_name = 'airport_details.csv'

# Construct the full path to the CSV file
file_path = os.path.join(script_dir, file_name)

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)
# Assume user_input is the airport entered by the user
user_input = 'london'

# Check if the user input matches any airport name in the DataFrame
matches = df[df['AirportName'].str.contains(user_input, case=False)]

if len(matches) == 0:
    print("Airport not found.")
else:
    # If multiple airports match, select the first one
    match = matches.iloc[0]
    airport_code = match['AirportCode']
    print(f"Airport code for '{user_input}' is '{airport_code}'.")

