# import needed libraries
import pandas as pd 
import numpy as np 
import re
import string 

# Local imports
# from source.constants import PUNCT_TO_REMOVE
import sys
import os
target = os.path.abspath(__file__)
while(target.split("\\")[-1]!="Road"):
    target = os.path.dirname(target)
sys.path.append(target) 

# For arabic diacritics
# pip install pyarabic 
from pyarabic.araby import strip_tashkeel, normalize_hamza
from pyarabic.araby import is_tashkeel, is_arabicrange

# For converting emojis and emot
# pip install emoji
import emoji
# pip install emot
import emot


def remove_diacritics(text: str) -> str:
    """
    Remove diacritics from Arabic text and reshape it to proper Arabic script.

    Args:
        text (str): The input Arabic text.

    Returns:
        str: The Arabic text with diacritics removed and reshaped to proper Arabic script.
    """
    if isinstance(text, str):
        # Normalize the text
        text = normalize_hamza(text)
        # Remove diacritics using regex
        diacritic_pattern = re.compile("[ًٌٍَُِّْ]+")
        text_without_diacritics = diacritic_pattern.sub("", text)
        # Reshape the text to proper Arabic script
        reshaped_text = ""
        for i, char in enumerate(text_without_diacritics):
            if is_arabicrange(char):
                if is_tashkeel(char):
                    reshaped_text += char
                else:
                    reshaped_text += strip_tashkeel(char)
            else:
                reshaped_text += char
        return reshaped_text
    else:
        return text

def remove_emojis_emoticons(text: str) -> str:
    """
    Remove emojis and emoticons from text.

    Args:
        text (str): The input text.

    Returns:
        str: The input text with emojis and emoticons removed.
    """
    # remove emojis
    text = emoji.demojize(text, delimiters=("", ""))
    
    # remove emoticons
    emo_obj = emot.EMOTICONS_EMO
    for emot1 in emo_obj:
        escaped_emot = re.escape(emot1)
        text = re.sub(u'({})'.format(escaped_emot), "_".join(emo_obj[emot1].replace(",", "").split()), text)
    
    return text

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

PUNCT_TO_REMOVE = string.punctuation + '؛،؟«»٪٫٬٭'
def remove_punctuations(text: str) -> str:
     """
     Remove punctuations from text.

     Args:
          text (str): The input text with punctuations.

     Returns:
          str: The input text with punctuations removed.
     """
     return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))

def remove_multimedia(text: str) -> str:
    """
    Remove multimedia (images, videos, etc.) from text.

    Args:
        text (str): The input text with multimedia.

    Returns:
        str: The input text with multimedia removed.
    """
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'pic\.twitter\.com/\S+', '', text)
    text = re.sub(r'@(\w+)', '', text)
    return text

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
