from typing import AsyncGenerator

import pytest
from fastapi import status
from httpx import AsyncClient

from app.main import app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_root_endpoint(
    client: AsyncClient,  # pylint: disable=redefined-outer-name
) -> None:
    response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello World"}


@pytest.mark.asyncio
async def test_healthcheck_endpoint(
    client: AsyncClient,  # pylint: disable=redefined-outer-name
) -> None:
    response = await client.get("/healthz")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}
