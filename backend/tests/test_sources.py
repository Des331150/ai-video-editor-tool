import io
import os
from pathlib import Path

import pytest
from httpx import AsyncClient

from app.config import settings


@pytest.mark.asyncio
async def test_upload_source(client: AsyncClient):
    create_resp = await client.post("/api/projects", json={"name": "Upload Test"})
    project_id = create_resp.json()["id"]

    file_content = b"fake video content"
    file = io.BytesIO(file_content)
    response = await client.post(
        f"/api/projects/{project_id}/sources",
        files={"file": ("test_video.mp4", file, "video/mp4")},
        data={"duration": 120.5},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["filename"] == "test_video.mp4"
    assert data["duration"] == 120.5
    assert data["file_size"] == len(file_content)
    assert data["media_type"] == "video"
    assert data["project_id"] == project_id
    assert "id" in data
    assert "created_at" in data

    # Verify the file was written to managed storage
    storage_dir = Path(settings.storage_path)
    expected_path = storage_dir / f"{data['id']}.mp4"
    assert expected_path.exists(), "Uploaded file not found in managed storage"
    assert expected_path.stat().st_size == len(file_content)


@pytest.mark.asyncio
async def test_upload_source_audio(client: AsyncClient):
    create_resp = await client.post("/api/projects", json={"name": "Audio Test"})
    project_id = create_resp.json()["id"]

    file = io.BytesIO(b"fake audio content")
    response = await client.post(
        f"/api/projects/{project_id}/sources",
        files={"file": ("podcast.mp3", file, "audio/mp3")},
        data={"duration": 1800.0},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["filename"] == "podcast.mp3"
    assert data["media_type"] == "audio"
    assert data["duration"] == 1800.0


@pytest.mark.asyncio
async def test_upload_source_unsupported_extension(client: AsyncClient):
    create_resp = await client.post("/api/projects", json={"name": "Ext Test"})
    project_id = create_resp.json()["id"]

    file = io.BytesIO(b"not a media file")
    response = await client.post(
        f"/api/projects/{project_id}/sources",
        files={"file": ("document.pdf", file, "application/pdf")},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_upload_source_project_not_found(client: AsyncClient):
    file = io.BytesIO(b"content")
    response = await client.post(
        "/api/projects/00000000-0000-0000-0000-000000000000/sources",
        files={"file": ("test.mp4", file, "video/mp4")},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_sources(client: AsyncClient):
    create_resp = await client.post("/api/projects", json={"name": "List Test"})
    project_id = create_resp.json()["id"]

    f1 = io.BytesIO(b"content a")
    await client.post(
        f"/api/projects/{project_id}/sources",
        files={"file": ("video_a.mp4", f1, "video/mp4")},
        data={"duration": 60.0},
    )
    f2 = io.BytesIO(b"content b")
    await client.post(
        f"/api/projects/{project_id}/sources",
        files={"file": ("audio_b.mp3", f2, "audio/mp3")},
        data={"duration": 30.0},
    )

    response = await client.get(f"/api/projects/{project_id}/sources")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    filenames = [s["filename"] for s in data]
    assert "video_a.mp4" in filenames
    assert "audio_b.mp3" in filenames


@pytest.mark.asyncio
async def test_list_sources_empty(client: AsyncClient):
    create_resp = await client.post("/api/projects", json={"name": "Empty Test"})
    project_id = create_resp.json()["id"]

    response = await client.get(f"/api/projects/{project_id}/sources")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_delete_source(client: AsyncClient):
    create_resp = await client.post("/api/projects", json={"name": "Delete Test"})
    project_id = create_resp.json()["id"]

    file = io.BytesIO(b"to delete")
    upload_resp = await client.post(
        f"/api/projects/{project_id}/sources",
        files={"file": ("delete_me.mp4", file, "video/mp4")},
    )
    source_id = upload_resp.json()["id"]

    response = await client.delete(
        f"/api/projects/{project_id}/sources/{source_id}"
    )
    assert response.status_code == 204

    list_resp = await client.get(f"/api/projects/{project_id}/sources")
    assert list_resp.json() == []


@pytest.mark.asyncio
async def test_delete_source_file_removed_from_storage(client: AsyncClient):
    create_resp = await client.post("/api/projects", json={"name": "Storage Test"})
    project_id = create_resp.json()["id"]

    file = io.BytesIO(b"file to delete")
    upload_resp = await client.post(
        f"/api/projects/{project_id}/sources",
        files={"file": ("storage_test.mp4", file, "video/mp4")},
    )
    source_id = upload_resp.json()["id"]

    await client.delete(f"/api/projects/{project_id}/sources/{source_id}")

    from app.config import settings
    storage_dir = Path(settings.storage_path)
    stored_files = list(storage_dir.glob(f"{source_id}.*"))
    assert len(stored_files) == 0


@pytest.mark.asyncio
async def test_delete_source_not_found(client: AsyncClient):
    create_resp = await client.post("/api/projects", json={"name": "NF Test"})
    project_id = create_resp.json()["id"]

    response = await client.delete(
        f"/api/projects/{project_id}/sources/"
        "00000000-0000-0000-0000-000000000000"
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_upload_source_without_duration(client: AsyncClient):
    create_resp = await client.post("/api/projects", json={"name": "No Dur"})
    project_id = create_resp.json()["id"]

    file = io.BytesIO(b"some content")
    response = await client.post(
        f"/api/projects/{project_id}/sources",
        files={"file": ("no_dur.mp4", file, "video/mp4")},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["duration"] is None
