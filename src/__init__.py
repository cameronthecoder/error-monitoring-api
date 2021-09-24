from quart import Quart, ResponseReturnValue
from quart_cors import cors
from databases import Database
from quart_schema import QuartSchema
from werkzeug.utils import import_string
from dotenv import load_dotenv
from quart import got_request_exception
from src.lib.api_error import APIError
from src.lib.database import create_database
import os, asyncio, sys

# Allow react app to communicate with API
ALLOWED_ORIGINS = ["http://localhost:3000"]


def create_app(testing=False):
    app = Quart(__name__)
    app = cors(app, allow_origin=ALLOWED_ORIGINS)
    QuartSchema(app, title="Error Monitoring API")

    # Register JSON error handler
    @app.errorhandler(APIError)  # type: ignore
    async def handle_api_error(error: APIError) -> ResponseReturnValue:
        for arg in error.args:
            print(arg)
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
            db = await create_database(app.config["DATABASE_URI"])
            with app.open_resource("schema.sql", "r") as file_:
                for command in file_.read().split(";"):
                    try:
                        await db.execute(command)
                    except:
                        print("fuck you")

        # run async
        asyncio.get_event_loop().run_until_complete(_inner())

    # Blueprints
    from src.blueprints.root import blueprint as root_blueprint
    from src.blueprints.projects import blueprint as projects_blueprint
    from src.blueprints.issues import blueprint as issues_blueprint

    app.register_blueprint(root_blueprint)
    app.register_blueprint(projects_blueprint)
    app.register_blueprint(issues_blueprint)

    return app
