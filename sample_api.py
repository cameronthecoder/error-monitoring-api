from quart import Quart, got_request_exception
from error_extension.quart_errors import QuartError

app = Quart(__name__)

QuartError(app, api_key='fb320860-2138-4807-9cc1-1f356ef14a57', server_host='http://localhost:8000').attach()


@app.route('/')
async def test():
    arr = [3, 3]
    arr[5]
    return 'hello world'