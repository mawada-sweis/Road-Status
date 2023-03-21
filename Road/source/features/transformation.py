# Standard library imports
import re
import os
import sys

# Related third party imports
import pandas as pd

# Reset the path to the parent folder to import any mudule we want
target = os.path.abspath(__file__)
while (target.split("\\")[-1] != "Road"):
    target = os.path.dirname(target)
sys.path.append(target)

# Local imports
from source.constants import QUESTION_REGEX, STATUS_OPEN_REGEX


def huara_matches(text: str) -> bool:
    """Check if the given text contains the Arabic word
        "حوارة" or its variations.

    Args:
        text (str): The text to search for matches.

    Returns:
        (bool): 1 if a match is found, 0 otherwise.
    """
    return int(bool(re.search(r"[حخ]وار[ه ة]", text)))


def categorize_message(row: pd.Series) -> str:
    """Categorize a message in a row of data as either a
        question or an answered message.

    Args:
        row (pd.Series): A row of data containing a 'message'
            and a 'reply' column.

    Returns:
        (str): 'question' if the 'message' column is a question,
            'answered' if the 'reply' column is not null, 'unknown' otherwise.
    """
    if pd.notna(row['reply']):
        return 'answered'
    message = row['message']
    return 'question' if QUESTION_REGEX.search(message) else 'unknown'


def get_status(reply: str) -> int:
    """Get the status of a reply message based on the presence
        of a specific regex pattern.

    Args:
        reply (str): The reply message to categorize.

    Returns:
        (int): 1 if the reply message contains the regex pattern
            for open status, 0 otherwise.
        Returns -1 if reply_msg is null or NaN.
    """
    
    return int(bool(STATUS_OPEN_REGEX.search(reply))) if pd.notna(reply) else -1
