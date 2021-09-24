import pytest
from quart import Quart


@pytest.mark.asyncio
async def test_root(app: Quart) -> None:
    test_client = app.test_client()
    response = await test_client.get("/")
    assert (await response.get_json())["message"] == "Hello World!"
