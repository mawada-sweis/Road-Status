from http import HTTPStatus
from fastapi import Request
from Road import app, logger
from source.features import data_cleaning as DC
from source.features import transformation as TF
import pandas as pd

@app.get("/health")
def _health_check(request: Request) -> dict:
    """Health check"""
    logger.info("Health check")
    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {},
    }

    logger.info(f"Health check Status-code :{HTTPStatus.OK} ")
    return response


def transformation_data(data: pd.DataFrame) -> pd.DataFrame:
    """Apply the huara_matches, categorize_message, and get_status functions
    on the given DataFrame and return the modified DataFrame.
    Args:
        data (pd.DataFrame): The DataFrame containing the 'message' and 'reply' columns.
    Returns:
        (pd.DataFrame): The modified DataFrame with three additional columns: 
            'huara_matches', 'message_type', and 'status'.
    """
    # new column for huara_matches
    data['huara_matches'] = data['message'].apply(huara_matches)
    
    # new column for message_type
    data['message_type'] = data.apply(categorize_message, axis=1)
    
    # new column for status
    data['status'] = data['reply'].apply(get_status)
    
    return data




