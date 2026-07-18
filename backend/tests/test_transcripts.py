import io
from dataclasses import dataclass

import pytest
from httpx import AsyncClient

from app.dependencies import get_transcriber
from app.main import app
from app.services.transcriber import WordTimestamp


class FakeTranscriberKnownWords:
    async def transcribe(self, file_path: str) -> list[WordTimestamp]:
        return [
            WordTimestamp("Hello", 0.0, 0.3),
            WordTimestamp("world", 0.3, 0.6),
        ]


class FakeTranscriberNoSpeech:
    async def transcribe(self, file_path: str) -> list[WordTimestamp]:
        return []


@pytest.mark.asyncio
async def test_transcript_created_on_upload(client: AsyncClient):
    fake = FakeTranscriberKnownWords()
    app.dependency_overrides[get_transcriber] = lambda: fake

    try:
        create_resp = await client.post("/api/projects", json={"name": "Transcribe Test"})
        project_id = create_resp.json()["id"]

        file = io.BytesIO(b"fake video content")
        upload_resp = await client.post(
            f"/api/projects/{project_id}/sources",
            files={"file": ("speech.mp4", file, "video/mp4")},
            data={"duration": 10.0},
        )
        assert upload_resp.status_code == 201
        source_id = upload_resp.json()["id"]

        transcript_resp = await client.get(
            f"/api/projects/{project_id}/sources/{source_id}/transcript"
        )
        assert transcript_resp.status_code == 200
        data = transcript_resp.json()
        assert data["source_id"] == source_id
        assert len(data["entries"]) == 2

        assert data["entries"][0]["word"] == "Hello"
        assert data["entries"][0]["start_time"] == 0.0
        assert data["entries"][0]["end_time"] == 0.3
        assert data["entries"][0]["position"] == 0

        assert data["entries"][1]["word"] == "world"
        assert data["entries"][1]["start_time"] == 0.3
        assert data["entries"][1]["end_time"] == 0.6
        assert data["entries"][1]["position"] == 1
    finally:
        app.dependency_overrides.pop(get_transcriber, None)


@pytest.mark.asyncio
async def test_transcript_empty_for_non_speech(client: AsyncClient):
    fake = FakeTranscriberNoSpeech()
    app.dependency_overrides[get_transcriber] = lambda: fake

    try:
        create_resp = await client.post("/api/projects", json={"name": "No Speech"})
        project_id = create_resp.json()["id"]

        file = io.BytesIO(b"music only content")
        upload_resp = await client.post(
            f"/api/projects/{project_id}/sources",
            files={"file": ("music.mp3", file, "audio/mp3")},
        )
        assert upload_resp.status_code == 201
        source_id = upload_resp.json()["id"]

        transcript_resp = await client.get(
            f"/api/projects/{project_id}/sources/{source_id}/transcript"
        )
        assert transcript_resp.status_code == 200
        data = transcript_resp.json()
        assert data["source_id"] == source_id
        assert data["entries"] == []
    finally:
        app.dependency_overrides.pop(get_transcriber, None)


@pytest.mark.asyncio
async def test_transcript_source_not_found(client: AsyncClient):
    create_resp = await client.post("/api/projects", json={"name": "Not Found"})
    project_id = create_resp.json()["id"]

    response = await client.get(
        f"/api/projects/{project_id}/sources/"
        "00000000-0000-0000-0000-000000000000/transcript"
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_transcript_project_not_found(client: AsyncClient):
    response = await client.get(
        "/api/projects/00000000-0000-0000-0000-000000000000/sources/"
        "00000000-0000-0000-0000-000000000000/transcript"
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_default_fake_transcriber_runs_on_upload(client: AsyncClient):
    create_resp = await client.post("/api/projects", json={"name": "Default"})
    project_id = create_resp.json()["id"]

    file = io.BytesIO(b"content")
    upload_resp = await client.post(
        f"/api/projects/{project_id}/sources",
        files={"file": ("test.mp4", file, "video/mp4")},
    )
    assert upload_resp.status_code == 201
    source_id = upload_resp.json()["id"]

    transcript_resp = await client.get(
        f"/api/projects/{project_id}/sources/{source_id}/transcript"
    )
    assert transcript_resp.status_code == 200
    data = transcript_resp.json()
    assert len(data["entries"]) > 0
    assert data["entries"][0]["word"] == "Hello"
