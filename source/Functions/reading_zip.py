"""
This module contains a function that unzips a zip-file of your choice
"""

# Import the necessary libraries
import zipfile
import pandas as pd

TARGET_URL = (
    "https://gitlab.com/adpro1/adpro2024/-/raw/main/Files/flight_data.zip?inline=false"
)
TARGET_FILE = "flight_data.zip"

def unzip(target_file: str) -> dict:
    """
    Unzips a file from an URL into your hard drive.

    Parameters
    ------------
    target_file: str
        A string containing the name of the file you wish to unzip.

    Returns
    ---------
    All csv files in the zip file in the form of a dictionary.
    """

    # Use 'with' to ensure the zip file is properly closed after its suite finishes
    with zipfile.ZipFile(target_file) as zip_contents:
        filelist = zip_contents.namelist()

        # Create a dictionary to store the dataframes
        dataframes_dict = {}

        # Loop through the file list
        for file in filelist:
            if file.endswith(".csv"):
                # Generate the dictionary key name by replacing ".csv" with "_df" in the filename
                key_name = file.replace(".csv", "_df")
                # Load the CSV file into a DataFrame and store it in the dictionary
                with zip_contents.open(file) as csv_file:
                    dataframes_dict[key_name] = pd.read_csv(csv_file)

    return dataframes_dict
