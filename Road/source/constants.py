# sourcery skip: use-fstring-for-concatenation
"""
This file might contain constant values that are used throughout the Project
e.g.
CLASS = 5

PLEASE WRITE CONSTANT VARIABLE NAME ALWAYS CAPITALIZED
"""
import re
import string 

COLUMNS_TO_KEEP = ['id', 'date', 'message', 'from_id', 'reply_to']
PUNCT_TO_REMOVE = string.punctuation + '؛،؟«»٪٫٬٭'

# define regular expressions for question message category
question_regex = re.compile(r"\?*|كيف|شو وضع|\؟*|في اشي|نمر|شي")
