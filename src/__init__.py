from quart import Quart, ResponseReturnValue
from quart_cors import cors
from quart_schema import QuartSchema
from werkzeug.utils import import_string
from src.lib.api_error import APIError
from src.lib.database import create_database
from error_extension.quart_errors import QuartErrorMonitor
import os, asyncio, sys, click

# Allow react app to communicate with API
ALLOWED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]


def create_app(testing=False):
    app = Quart(__name__)
    app = cors(app, allow_origin=ALLOWED_ORIGINS)
    QuartSchema(app)
    app.monitor = QuartErrorMonitor(
        app,
        'fb320860-2138-4807-9cc1-1f356ef14a57',
        excluded_keys=["POSTGRES_PASSWORD", "POSTGRES_USER"],
        server_host="http://localhost:5000",
    ).attach()

    # Register JSON error handler
    @app.errorhandler(APIError)  # type: ignore
    async def handle_api_error(error: APIError) -> ResponseReturnValue:
        return {"code": error.code}, error.status_code

    quart_env = os.getenv("QUART_ENV", None)

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
            db = await create_database(app.config["DATABASE_URI"], set_codecs=False)
            with open(os.getcwd() + "/src/schema.sql", "r") as file_:
                for command in file_.read().split(";"):
                    await db.execute(command)

        # run async
        asyncio.get_event_loop().run_until_complete(_inner())

    @app.cli.command("create_fake_error")
    @click.argument("api_key")
    def create_fake_error(api_key) -> None:
        """
        Create fake error for a project
        """

        async def _inner() -> None:
            client = app.test_client()
            await client.get(f"/api/projects/{api_key}/issues/gen/")

        asyncio.get_event_loop().run_until_complete(_inner())

    @app.cli.command("drop_db")
    def drop_db() -> None:
        async def _inner() -> None:
            db = await create_database(app.config["DATABASE_URI"], set_codecs=False)
            stmt = """
                DROP TABLE IF EXISTS projects CASCADE;
                DROP TABLE IF EXISTS frames CASCADE;
                DROP TABLE IF EXISTS issues CASCADE;
                DROP TABLE IF EXISTS issues_frames CASCADE;
                DROP TYPE IF EXISTS status;
            """
            queries = stmt.split(';')
            for query in queries:
                await db.execute(query)

        asyncio.get_event_loop().run_until_complete(_inner())

    # Blueprints
    from src.blueprints.root import blueprint as root_blueprint
    from src.blueprints.projects import blueprint as projects_blueprint
    from src.blueprints.issues import blueprint as issues_blueprint

    app.register_blueprint(root_blueprint)
    app.register_blueprint(projects_blueprint)
    app.register_blueprint(issues_blueprint)

    return app
