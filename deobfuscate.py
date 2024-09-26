import netCDF4 as nc
import numpy as np
import json
import csv
from tkinter import Tk, simpledialog
from tkinter.filedialog import askopenfilename, asksaveasfilename

# Function to select the input NetCDF file
def select_nc_file():
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = askopenfilename(title="Select NetCDF File", filetypes=[("NetCDF Files", "*.nc")])

    if not file_path:
        print("No file selected.")
        return None
    return file_path

# Function to select the output format (JSON or CSV)
def select_output_format():
    root = Tk()
    root.withdraw()  # Hide the root window
    # Prompt the user for output format
    format_choice = simpledialog.askstring("Output Format", "Enter the format (json/csv):").lower()

    if format_choice not in ['json', 'csv']:
        print("Invalid format. Please enter 'json' or 'csv'.")
        return None
    return format_choice

# Function to choose where to save the file
def save_output_file(format_choice):
    root = Tk()
    root.withdraw()  # Hide the root window

    file_types = {
        'json': [("JSON Files", "*.json")],
        'csv': [("CSV Files", "*.csv")]
    }

    # Ask the user to choose where to save the file
    file_path = asksaveasfilename(title=f"Save as {format_choice.upper()}", defaultextension=f".{format_choice}",
                                  filetypes=file_types[format_choice])

    if not file_path:
        print("Save operation cancelled.")
        return None
    return file_path

# Function to convert NetCDF to JSON
def convert_nc_to_json(data, json_file_path):
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data successfully saved to {json_file_path} as JSON.")

# Function to convert NetCDF to CSV
def convert_nc_to_csv(data, csv_file_path):
    lats = data["latitude"]
    lons = data["longitude"]
    wind_speed = data["wind_speed"]

    # Open CSV file for writing
    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write header
        writer.writerow(["latitude", "longitude", "wind_speed"])

        # Iterate over latitude and longitude, assuming wind_speed is a 2D array
        for i in range(len(lats)):
            for j in range(len(lons)):
                writer.writerow([lats[i], lons[j], wind_speed[i][j]])

    print(f"Data successfully saved to {csv_file_path} as CSV.")

# Function to extract data from NetCDF file
def extract_nc_data(nc_file_path):
    # Step 2: Load the NetCDF file
    dataset = nc.Dataset(nc_file_path)

    # Step 3: Extract variables and convert them to lists
    lats = dataset.variables['lat'][:].tolist()
    lons = dataset.variables['lon'][:].tolist()
    time = dataset.variables['time'][:].tolist()
    wind_speed = dataset.variables['wind_speed'][0, :, :].filled(-999.0).tolist()
    quality_level = dataset.variables['quality_level'][0, :, :].filled(-128).tolist()

    # Create a dictionary to store the data in a generic format
    data = {
        "time": time,
        "latitude": lats,
        "longitude": lons,
        "wind_speed": wind_speed,
        "quality_level": quality_level
    }
    return data

# Main function to handle the conversion
def convert_nc_to_multiple_formats():
    # Step 1: Select the .nc file
    nc_file_path = select_nc_file()
    if not nc_file_path:
        return

    # Step 2: Extract the data from the NetCDF file
    data = extract_nc_data(nc_file_path)

    # Step 3: Choose the output format
    format_choice = select_output_format()
    if not format_choice:
        return

    # Step 4: Choose where to save the output file
    output_file_path = save_output_file(format_choice)
    if not output_file_path:
        return

    # Step 5: Convert and save in the chosen format
    if format_choice == 'json':
        convert_nc_to_json(data, output_file_path)
    elif format_choice == 'csv':
        convert_nc_to_csv(data, output_file_path)

# Run the converter
convert_nc_to_multiple_formats()
