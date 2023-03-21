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
    number_of_messages: int, file_path: str = "Road/data/interim/cleaned_data.csv"
) -> pd.DataFrame:
    """
    Reads n messages from a CSV file and returns them as a pandas DataFrame.

    Args:
        number_of_messages (int): The number of messages to read from the file.
        file_path (str, optional): The path to the CSV file to read. Defaults to "Road/data/interim/cleaned_data.csv".

    Returns:
        pd.DataFrame: A pandas DataFrame containing the read messages.

    Raises:
    - FileNotFoundError: If the file specified in file_path cannot be found.
    """
    try:
        data = pd.read_csv(file_path, nrows=number_of_messages)
        data.drop("Unnamed: 0", axis=1, inplace=True)  # remove the 'Unnamed: 0' column
    except FileNotFoundError as e:
        logger.exception(f"Error reading file {file_path}: {e}")
        raise
    except KeyError as e:
        pass  # skip the error if Unnamed: 0 not found in the dataframe columns
    return data
