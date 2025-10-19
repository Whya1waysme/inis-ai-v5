from __future__ import annotations

import os
import asyncio
from typing import Any

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app
from app.config import settings


@pytest.fixture(scope="session", autouse=True)
def setup_env():
    # No-op in stateless mode
    pass


def test_healthz():
    client = TestClient(app)
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_camera_settings():
    client = TestClient(app)
    payload = {
        "scene_type": "portrait",
        "lighting": "daylight",
        "motion": "none",
        "desired_depth_of_field": "shallow",
    }
    r = client.post("/camera-settings", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["iso"] in (100, 200)
    assert data["aperture"] <= 2.8


@pytest.mark.asyncio
async def test_storyboards_list_empty():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/storyboards", params={"script_id": 99999})
        assert r.status_code == 200
        assert r.json()["items"] == []
