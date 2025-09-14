import pytest
from httpx import AsyncClient
from fastapi import FastAPI


@pytest.mark.asyncio
async def test_healthz():
    from app.main import app

    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get("/healthz")
        assert res.status_code == 200
        assert res.json()["status"] == "ok"

