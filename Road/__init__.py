from fastapi import FastAPI,Request
from http import HTTPStatus
import logging
app = FastAPI(
    title="Road Status API",
    description="",
    version=0.1
)
logger = logging.getLogger(__name__)
logging.basicConfig(filename='Road/logs/RouadStatus.log',level=logging.DEBUG)


from Road.endpoints import endpoints