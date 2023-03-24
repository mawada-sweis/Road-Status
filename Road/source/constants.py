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
QUESTION_REGEX = re.compile(r"\?*|كيف|شو وضع|\؟*|في اشي|نمر|شي|\!*")
STATUS_OPEN_REGEX = re.compile(r"(سا+لك[هة]?(ين)?|من[يا]ح[هة]?|ما في ا?شي|فاضي[هة]?|ازم[ةه]|ماشية?|فا?تح[هة]?)")
