from quart import Blueprint

blueprint = Blueprint("root", __name__)


@blueprint.get("/")
async def hello_world():
    """
    Hello World! route
    """
    return {"message": "Hello World!"}
