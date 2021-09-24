from typing import AsyncGenerator
from quart import Quart
from src import create_app
import pytest


@pytest.fixture(name="app", scope="function")
async def _app() -> AsyncGenerator[Quart, None]:
    app = create_app()
    
    async with app.test_app():
        yield app
