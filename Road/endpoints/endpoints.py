from http import HTTPStatus
from fastapi import Request
from Road import app, logger
from source.features import data_cleaning as DC
from source.features import transformation as TF

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


def clean_and_transform_data(data):
    # Convert float message values to empty strings
    data["message"] = data["message"].apply(lambda x: "" if isinstance(x, float) else x)

    # Clean message text
    data["message"] = data["message"].apply(DC.remove_diacritics)
    data["message"] = data["message"].apply(DC.remove_emojis_emoticons)
    data["message"] = data["message"].apply(DC.remove_urls)
    data["message"] = data["message"].apply(DC.remove_phone_numbers)
    data["message"] = data["message"].apply(DC.remove_punctuations)
    data["message"] = data["message"].apply(DC.remove_multimedia)

    # Drop rows with empty message text
    data = data.drop(data[data["message"] == ""].index)

    # Categorize messages
    data["category"] = data.apply(TF.categorize_message, axis=1)

    # Determine Huara barrier status
    data["open_status"] = data["reply"].apply(TF.get_status)

    return data




