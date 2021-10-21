from dataclasses import dataclass
from datetime import datetime
from quart import Blueprint, request
from quart_schema import validate_response


blueprint = Blueprint("issues", __name__, url_prefix="/api")

error = ''

@blueprint.post("/projects/issues/")
async def testing():
    global error
    data = (await request.get_json())
    error = data
    return '', 200

@blueprint.get('/error/')
async def error():
    global error
    return error
