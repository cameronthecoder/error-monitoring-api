from quart import Blueprint
#from dataclasses import dataclass, asdict
#from quart_schema import validate_request
#from quart_schema.extension import tag
#from quart_schema.validation import validate_response

root = Blueprint("root", __name__)

@root.get("/")
async def hello_world():
    """
    Hello World! route
    """
    return {"message": "Hello World!"}


