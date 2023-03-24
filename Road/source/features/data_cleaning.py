# import needed libraries
import pandas as pd 
import numpy as np 
import re
import string 

# Local imports
from source.constants import PUNCT_TO_REMOVE
import sys
import os
target = os.path.abspath(__file__)
while(target.split("\\")[-1]!="Road"):
    target = os.path.dirname(target)
sys.path.append(target) 

# For arabic diacritics 
from pyarabic.araby import strip_tashkeel, is_tashkeel, is_arabicrange

# For converting emojis
import emoji


def remove_diacritics(text: str) -> str:
    """
    Remove diacritics from Arabic text.

    Args:
        text (str): The input Arabic text.

    Returns:
        str: The Arabic text with diacritics removed.
    """
    # initialize an empty string to hold the text without diacritics
    text_without_diacritics = ""
    for char in text:
        # check if the character is in the Arabic Unicode range
        if is_arabicrange(char):
            # check if the character is a diacritic
            if is_tashkeel(char):
                # if it is a diacritic, remove it using the strip_tashkeel function
                text_without_diacritics += strip_tashkeel(char)
            else:
                # if it is not a diacritic, append it to the text without diacritics
                text_without_diacritics += char
        else:
            # if the character is not in the Arabic Unicode range, append it to the text without diacritics
            text_without_diacritics += char
    
    return text_without_diacritics

def remove_emojis(text: str) -> str:
    """
    Remove emojis from text.

    Args:
        text (str): The input text.

    Returns:
        str: The input text with emojis and emoticons removed.
    """
    new_text = ''
    for character in text:
        if not emoji.is_emoji(character):
            new_text += character
    return new_text

def remove_urls(text: str) -> str:
    """
    Remove URLs from text.

    Args:
        text (str): The input text with URLs.

    Returns:
        str: The input text with URLs removed.
    """
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)

def remove_phone_numbers(text: str) -> str:
    """
    Remove phone numbers from text.

    Args:
        text (str): The input text with phone numbers.

    Returns:
        str: The input text with phone numbers removed.
    """
    text = re.sub(r'(\+?\d{2,4}[ -]?)?\d{9,10}', '', text)
    return text

def remove_punctuations(text: str) -> str:
     """
     Remove punctuations from text.

     Args:
          text (str): The input text with punctuations.

     Returns:
          str: The input text with punctuations removed.
     """
     return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))


def map_reply_messages(data: pd.DataFrame) -> pd.DataFrame:
    """
    Map each message to its corresponding reply message in the "reply" column, and delete any rows with non -1 reply_to values.

    Args:
        data (pandas.DataFrame): The input DataFrame containing message data.

    Returns:
        pandas.DataFrame: The modified DataFrame with mapped reply messages and deleted rows.
    """
    # create an empty dictionary to store message-reply mappings
    message_reply_dict = {}

    # iterate over each row in the dataframe
    for i, row in data.iterrows():
        # check if the row has a valid reply_to value
        if row["reply_to"] != -1:
            # store the message-reply mapping in the dictionary
            message_reply_dict[row["reply_to"]] = row["message"]

    # update the reply column with the corresponding reply message
    data["reply"] = data["id"].map(message_reply_dict)

    # delete any rows with non -1 reply_to values
    data = data[data["reply_to"] == -1]

    return data