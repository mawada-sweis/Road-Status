# Standard library imports
from source.constants import COLUMNS_TO_KEEP
import ast
import sys
import os

# Related third party imports
import pandas as pd

# Reset the path to the parent folder to import any mudule we want
target = os.path.abspath(__file__)
while (target.split("\\")[-1] != "Road"):
    target = os.path.dirname(target)
sys.path.append(target)

# Local imports


def delete_unnecessery_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Remove all unnecessary columns except id, date, message,
    from_id and reply_to columns.

    Args:
        data (pd.DataFrame): The dataframe that will be modify.

    Returns:
        (pd.DataFrame): a new DataFrame with only the columns
            specified in COLUMNS_TO_KEEP list.
    """
    return data[COLUMNS_TO_KEEP].copy()


def extract_dates(date: pd.Series) -> tuple(pd.Series):
    """Extract year, month, day, hour, minute, and second values
    from the date series.

    Args:
        date (pd.Series): The date column to turn it into useful columns

    Returns:
        tuple(pd.Series): a tuple of six Pandas Series, each corresponding
            to a different aspect of the original dates:
            year, month, day, hour, minute, and second.
    """
    date = pd.to_datetime(date)
    year = date.dt.year
    month = date.dt.month
    day = date.dt.day
    hour = date.dt.hour
    minute = date.dt.minute
    second = date.dt.second

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
