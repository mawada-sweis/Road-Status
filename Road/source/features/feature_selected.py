# Import constant values
from source.constants import COLUMNS_TO_KEEP
# Necessary libraries
import pandas as pd
import ast
import sys
import os
# Reset the path to the parent folder to import any mudule we want
target = os.path.abspath(__file__)
while (target.split("\\")[-1] != "Road"):
    target = os.path.dirname(target)
sys.path.append(target)


def delete_unnecessery_columns(data: pd.DataFrame) -> None:
    """Remove all unnecessary columns except id, date, message,
    from_id and reply_to columns.

    Args:
        data (pd.DataFrame): The dataframe that will be modify.

    Returns:
        None
    """
    return data[COLUMNS_TO_KEEP].copy()

def extract_dates(date: pd.Series) -> None:
    """Extract year, month, day, hour, minute, and second values
    from the date series.

    Args:
        date (pd.Series): The date column to turn it into useful columns

    Returns:
        None
    """
    year = pd.to_datetime(date).dt.year
    month = pd.to_datetime(date).dt.month
    day = pd.to_datetime(date).dt.day
    hour = pd.to_datetime(date).dt.hour
    minute = pd.to_datetime(date).dt.minute
    second = pd.to_datetime(date).dt.second

    return (year, month, day, hour, minute, second)


def extract_id(json_string: str, target_id: str) -> int:
    """Extracts an ID from a JSON string.

    Args:
        json_string: A JSON string containing one or more IDs.
        target_it: The index of the desired ID in the JSON string.

    Returns:
        (int): The extracted ID, or -1 if the input is null or not a string.
    """
    if isinstance(json_string, str):
        # Get the target ID after convert the string to a dictionary
        return ast.literal_eval(json_string.replace("'", "\""))[target_id]
    elif pd.isna(json_string):
        return -1
