from http import HTTPStatus
from fastapi import Request
from Road import app,logger
@app.get("/health")
def _health_check(request:Request)->dict:
    """Health check"""
    logger.info("Health check")
    response = {
        "message":HTTPStatus.OK.phrase,
        "status-code":HTTPStatus.OK,
        "data":{}
    }
    
    logger.info(f"Health check Status-code :{HTTPStatus.OK} ")
    return response
