from quart import Quart, ResponseReturnValue
from quart_cors import cors
from databases import Database
from quart_schema import QuartSchema
from werkzeug.utils import import_string
from dotenv import load_dotenv
from src.lib.api_error import APIError
from src.lib.database import create_database
import os, asyncio


def create_app(testing=False):
    app = Quart(__name__)
    app = cors(app, allow_origin=['http://localhost:3000'])
    QuartSchema(app)

    # Register JSON error handler
    @app.errorhandler(APIError)  # type: ignore
    async def handle_api_error(error: APIError) -> ResponseReturnValue:
        return {"code": error.code}, error.status_code

    quart_env = os.getenv("QUART_ENV", None)


    # TODO: use config from pgjones book

    if testing:
        cfg = import_string("src.config.TestingConfig")()
    elif quart_env == "development":
        cfg = import_string("src.config.DevelopmentConfig")()
    elif quart_env == "testing":
        cfg = import_string("src.config.TestingConfig")()
    else:
        cfg = import_string("src.config.ProductionConfig")()
    app.config.from_object(cfg)

    @app.before_serving
    async def startup() -> None:
        app.db = await create_database(app.config["DATABASE_URI"])

    @app.after_serving
    async def disconnect_db() -> None:
        await app.db.disconnect()

    @app.cli.command("init_db")
    def init_db() -> None:
        """
        Add all of the tables to the database
        """

        async def _inner() -> None:
            await app.db.connect()
            with app.open_resource("schema.sql", "r") as file_:
                for command in file_.read().split(";"):
                    await app.db.execute(command)

        # run async
        asyncio.run(_inner())

    # Blueprints
    from src.blueprints.root import root as root_blueprint

    app.register_blueprint(root_blueprint)

    return app
