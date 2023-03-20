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


def huara_matches(text):
    return 1 if re.search(r"[حخ]وار[ه ة]", text) else 0


def _categorize_message(text):
    return 'question' if QUESTION_REGEX.search(text) else 'unknown'


def categorize_message(row):
    if pd.isna(row['reply']):
        message =row['message']
        return _categorize_message(message)
    else:
        return 'answered'


def _categorize_status(text):
    return 1 if STATUS_OPEN_REGEX.search(text) else 0


def get_status(reply_msg):
    return _categorize_status(reply_msg) if pd.notna(reply_msg) else -1
