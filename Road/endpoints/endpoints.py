from http import HTTPStatus
from fastapi import Request
from Road import app, logger
from Road.source.utils import read_n_from_file


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


@app.get("/get_messages")
def __get_n_messages(number_of_messages: int = 5) -> dict:
    """
    Returns the latest n messages from a data source.

    Parameters:
        number_of_messages (int): The number of messages to return. Defaults to 5.

    Returns:
        A dictionary with the following keys:
            - message: The HTTP status message.
            - status-code: The HTTP status code.
            - data: A list of dictionaries containing the message data.
    """
    try:
        messages = read_n_from_file(number_of_messages)
    except FileNotFoundError as e:
        return {
            "message": HTTPStatus.NOT_FOUND.phrase,
            "status-code": HTTPStatus.NOT_FOUND,
            "data": {},
        }
    messages_dict = messages.to_dict("records")

    logger.info(f"Retrieved {len(messages_dict)} messages from file.")
    # Convert float values to strings to ensure JSON compliance (the numbers in data)
    # TODO  you should handle this case the the preprocessing step by
    # converting the numbers to string if its not needed to be fload aka id
    # So i can refactor this function
    for message in messages_dict:
        for key, value in message.items():
            if isinstance(value, float):
                message[key] = str(value)

    return {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": messages_dict,
    }
