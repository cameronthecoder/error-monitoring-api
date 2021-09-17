from quart import Quart
from quart_cors import cors
from databases import Database
from quart_schema import QuartSchema
from werkzeug.utils import import_string
from dotenv import load_dotenv

# We need to load from the .env file here so we can get the current environment
import os
import asyncio


def create_app(testing=False):
    app = Quart(__name__)
    app = cors(app)
    QuartSchema(app, title="IssueAware API")

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

    database = Database(app.config["DATABASE_URI"])

    @app.before_serving
    async def _create_db_pool() -> None:
        try:
            await database.connect()
            print(quart_env)
            app.logger.info(
                f'Connected to database {app.config["POSTGRES_DATABASE"]} on port {app.config["POSTGRES_PORT"]}'
            )
        except Exception as e:
            app.logger.error(e)
        if database.is_connected:
            app.db = database

    @app.after_serving
    async def disconnect_db():
        if database.is_connected:
            app.logger.info("Disconnected")
            await database.disconnect()

    @app.cli.command("init_db")
    def init_db() -> None:
        """
        Add all of the tables to the database
        """

        async def _inner() -> None:
            await database.connect()
            with app.open_resource("schema.sql", "r") as file_:
                for command in file_.read().split(";"):
                    await database.execute(command)

        # run async
        asyncio.run(_inner())

    # Blueprints
    from src.api import root

    app.register_blueprint(root.root)

    return app
