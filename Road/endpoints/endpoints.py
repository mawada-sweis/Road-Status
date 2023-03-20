from http import HTTPStatus
from fastapi import Request
from Road import app, logger

# DC ==> data_cleaning in source.features
# FS ==> feature_selected in source.features


@app.get("/health")
def _health_check(request: Request) -> dict:
    """Health check"""
    logger.info("Health check")
    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {}
    }

    logger.info(f"Health check Status-code :{HTTPStatus.OK} ")
    return response


@app.post("/preprocessing")
def preprocessing_data(data: pd.DataFrame):

    """
    This function performs preprocessing on a Pandas DataFrame containing messaging data. The function applies a series
    of transformations to the DataFrame, including deleting unnecessary columns, extracting date information, and
    cleaning the text in the "message" column. The function also maps reply messages to their corresponding original
    messages.

    Args:
        data (pd.DataFrame): A Pandas DataFrame containing messaging data.
       
       
    Returns:
        pd.DataFrame: A processed Pandas DataFrame.
    """

    # This function deletes unnecessary columns from the input DataFrame.
    data = FS.delete_unnecessery_columns(data)

    # This function extracts date information from the "date" column of the DataFrame and adds it as new columns.
    (
    data['year'],
    data['month'],
    data['day'],
    data['hour'],
    data['minute'],
    data['second'],
    ) = FS.extract_dates(date=data['date'])

    # This function extracts the user ID from the "from_id" column.
    data['from_id'] = data['from_id'].apply(
    lambda info: FS.extract_id(json_string=info, target_id='user_id'))

    # This function extracts the reply message ID from the "reply_to" column.
    data['reply_to'] = data['reply_to'].apply(lambda info: FS.extract_id(json_string=info, target_id='reply_to_msg_id'))

    # This function cleans the text in the "message" column.
    data['message'] = data["message"].apply(lambda message: DC.clean_text(message))

    # This function maps reply messages to their corresponding original messages.
    data = DC.map_reply_messages(data)

    # This line removes rows where the value in the specified column is an empty string, and resets the DataFrame index.
    data = data[data[column_name]!= ""].reset_index()

    # This line drops the "reply_to" and "date" columns from the DataFrame.
    data.drop(columns=["reply_to", "date"], axis=1, inplace=True)

    # Finally, the processed DataFrame is returned.
    return data