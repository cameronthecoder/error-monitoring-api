from error_extension.client import Client
from quart import Quart, got_request_exception, request


class QuartError(object):
    def __init__(
        self, quart_app: Quart, api_key: str, server_host: str = "http://localhost:8000"
    ) -> None:
        self.quart_app = quart_app
        self.sender = None
        self.api_key = api_key
        self.server_host = server_host
        #self.quart_app.logger.addHandler

        got_request_exception.connect(self.handle_exception, quart_app)
        quart_app.extensions["error_handler"] = self
            

    async def handle_exception(self, sender, exception: Exception, **extra) -> None:
        request_data = self.get_request_data()
        env_data = self.quart_app.config
        self.sender.send_exception(exception, type(exception), request_data, env_data)

    def get_request_data(self) -> dict:
        try:
            req =  {
                "headers": dict(request.headers),
                "path": request.path,
                "url": request.url,
                "host": request.host,
                "args": request.args,
                "method": request.method,
                "cookies": request.cookies,
            }
            return {}
        except:
            return {}

    def attach(self) -> Client:
        if not hasattr(self.quart_app, "extensions"):
            self.quart_app.extensions = {}
        self.sender = Client(self.api_key, self.server_host)

        return self.sender
