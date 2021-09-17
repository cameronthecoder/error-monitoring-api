from quart import Blueprint

root = Blueprint('root', __name__)

@root.get('/')
async def index():
    """
    Root index
    """
    return {'message': 'Hello World!'}