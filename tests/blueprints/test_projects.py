import pytest
from quart import Quart


@pytest.mark.asyncio
async def test_select_projects(app: Quart) -> None:
    test_client = app.test_client()
    response = await test_client.get("/api/projects/")
    assert response.status_code == 200
