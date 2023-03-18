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
from source.constants import question_regex


def huara_matches(text):
    return 1 if re.search(r"[ح خ]وار[ه ة]", text) else 0


def reply_message(reply_to_list, id_list, message_list):
    for i, reply_to_id in enumerate(reply_to_list):
        if reply_to_id != -1:
            for j in range(i):
                if id_list[j] == reply_to_id:
                    reply_to_list[j] = message_list[i]
                    break


def _categorize_message(text):
    return 'question' if question_regex.search(text) else 'unknown'


def categorize_message(reply_column, message_column):
    categorized = []
    for i, reply in enumerate(reply_column):
        if isinstance(reply, str):
            categorized.append('answered')
        else:
            categorized.append(_categorize_message(message_column[i]))
    return pd.Series(categorized)
