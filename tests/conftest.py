from src.lib.database import create_database
from typing import AsyncGenerator
from quart import Quart
from src import create_app
import pytest


@pytest.fixture(name="app", scope="function")
async def _app() -> AsyncGenerator[Quart, None]:
    app = create_app()
    db = await create_database(app.config["DATABASE_URI"])
    with app.open_resource("schema.sql", "r") as file_:
        for command in file_.read().split(";"):
            await db.execute(command)

    async with app.test_app():
        yield app
