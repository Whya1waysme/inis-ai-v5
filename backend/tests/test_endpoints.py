from __future__ import annotations

from typing import Any, List

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.clients.openai_client import OpenAIClient
from app.clients.higgsfield_client import HiggsfieldClient


@pytest.fixture
def client():
    return TestClient(app)


def test_generate_script_success(client, monkeypatch):
    def fake_generate_script(self, prompt: str, **kwargs: Any) -> str:
        assert "hero" in prompt or prompt
        return "INT. ROOM - DAY\nA simple test script."

    monkeypatch.setattr(OpenAIClient, "generate_script", fake_generate_script, raising=True)

    r = client.post(
        "/generate-script",
        json={
            "prompt": "Write a short scene about a hero.",
            "title": "Test Scene",
            "temperature": 0.2,
            "max_tokens": 200,
            "language": "en",
        },
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert "content" in data
    assert "A simple test script" in data["content"]


def test_generate_storyboard_success(client, monkeypatch):
    # Prepare a script first (mock OpenAI)
    monkeypatch.setattr(
        OpenAIClient,
        "generate_script",
        lambda self, prompt, **kwargs: "Test script for storyboard",
        raising=True,
    )
    r = client.post("/generate-script", json={"prompt": "Create storyboard."})
    assert r.status_code == 200

    async def fake_generate_images(self, prompt: str, num_images: int = 1, **kwargs: Any) -> List[str]:
        return [
            "https://example.com/img1.png",
            "https://example.com/img2.png",
        ]

    monkeypatch.setattr(HiggsfieldClient, "generate_images", fake_generate_images, raising=True)

    r2 = client.post(
        "/generate-storyboard",
        json={
            "prompt": "A scene with two images",
            "num_images": 2,
            "width": 512,
            "height": 288,
            "quality": "high",
        },
    )
    assert r2.status_code == 200, r2.text
    data = r2.json()
    assert "storyboards" in data
    assert len(data["storyboards"]) == 2

    # Verify listing
    r3 = client.get("/storyboards", params={"script_id": 123})
    assert r3.status_code == 200
    assert r3.json()["items"] == []
