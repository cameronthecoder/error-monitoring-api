from quart import Blueprint
from quart_schema import validate_response


blueprint = Blueprint("issues", __name__, url_prefix="/api")


@blueprint.route("/issues/")
async def testing():
    # TODO: get issues from database
    return "Hello WORLD"
