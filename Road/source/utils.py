"""
this file could contain all functions that we want to use  in the project.
e.g.
def function_name(parameter_name:type)->return_type:
    local_variable=0
    return
"""
import pandas as pd
from Road import logger


def read_n_from_file(
        number_of_messages: int=5,
        file_path: str="Road/data/raw/data.csv") -> pd.DataFrame:
    """
    Reads n messages from the end of a CSV file and returns them as a pandas DataFrame.

    Args:
        number_of_messages (int): The number of messages to read from the file. Defaults to 5
        file_path (str, optional): The path to the CSV file to read. Defaults to "Road/data/interim/cleaned_data.csv".

    Returns:
        pd.DataFrame: A pandas DataFrame containing the read messages.

    Raises:
    - FileNotFoundError: If the file specified in file_path cannot be found.
    """
    try:
        data = pd.read_csv(file_path)
        last_n_rows = data.tail(number_of_messages)
    except FileNotFoundError as e:
        logger.exception(f"Error reading file {file_path}: {e}")
        raise
    return last_n_rows
