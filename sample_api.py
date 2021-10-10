from quart import Quart, got_request_exception
from error_extension.quart_errors import QuartError

app = Quart(__name__)

QuartError(app, api_key='da86f346-0c01-44dd-814c-53e5ff14cd75', server_host='http://localhost:5000').attach()


@app.route('/')
async def test():
    arr = [3, 3]
    arr[5]
    return 'hello world'