import { useCallback, useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getProject } from "../api/projects";
import { listSources, uploadSource, deleteSource } from "../api/sources";
import type { Project } from "../api/projects";
import type { SourceMedia } from "../api/sources";

function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function formatDuration(seconds: number | null): string {
  if (seconds === null) return "--";
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

function getFileDuration(file: File): Promise<number | undefined> {
  return new Promise((resolve) => {
    if (!file.type.startsWith("video/") && !file.type.startsWith("audio/")) {
      resolve(undefined);
      return;
    }
    const url = URL.createObjectURL(file);
    const media = document.createElement(file.type.startsWith("video/") ? "video" : "audio");
    media.preload = "metadata";
    media.onloadedmetadata = () => {
      URL.revokeObjectURL(url);
      resolve(media.duration);
    };
    media.onerror = () => {
      URL.revokeObjectURL(url);
      resolve(undefined);
    };
    media.src = url;
  });
}

export default function ProjectEditor() {
  const { projectId } = useParams<{ projectId: string }>();
  const navigate = useNavigate();
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [sources, setSources] = useState<SourceMedia[]>([]);
  const [uploading, setUploading] = useState(false);

  const loadSources = useCallback(async () => {
    if (!projectId) return;
    try {
      const data = await listSources(projectId);
      setSources(data);
    } catch (err) {
      console.error("Failed to load sources", err);
    }
  }, [projectId]);

  useEffect(() => {
    if (!projectId) return;
    getProject(projectId)
      .then(setProject)
      .catch((err) => {
        console.error("Failed to load project", err);
        navigate("/");
      })
      .finally(() => setLoading(false));
  }, [projectId, navigate]);

  useEffect(() => {
    if (!projectId) return;
    loadSources();
  }, [projectId, loadSources]);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !projectId) return;
    setUploading(true);
    try {
      const duration = await getFileDuration(file);
      await uploadSource(projectId, file, duration);
      await loadSources();
    } catch (err) {
      console.error("Upload failed", err);
    } finally {
      setUploading(false);
      e.target.value = "";
    }
  };

  const handleDelete = async (sourceId: string) => {
    if (!projectId) return;
    try {
      await deleteSource(projectId, sourceId);
      setSources((prev) => prev.filter((s) => s.id !== sourceId));
    } catch (err) {
      console.error("Delete failed", err);
    }
  };

  if (loading) return <div className="loading">Loading project...</div>;
  if (!project) return null;

  return (
    <div className="project-editor">
      <header className="editor-header">
        <button className="btn btn-secondary" onClick={() => navigate("/")}>
          &larr; Back
        </button>
        <h1>{project.name}</h1>
      </header>
      <div className="editor-layout">
        <div className="editor-panel sources-panel">
          <h2>Source Media</h2>
          <div className="upload-area">
            <label className="btn btn-primary upload-btn">
              {uploading ? "Uploading..." : "+ Upload Media"}
              <input
                type="file"
                accept="video/*,audio/*"
                onChange={handleUpload}
                disabled={uploading}
                hidden
              />
            </label>
          </div>
          {sources.length === 0 ? (
            <p className="placeholder-text">No source media uploaded yet.</p>
          ) : (
            <ul className="source-list">
              {sources.map((source) => (
                <li key={source.id} className="source-item">
                  <div className="source-info">
                    <span className="source-name">{source.filename}</span>
                    <span className="source-meta">
                      {formatDuration(source.duration)} &middot;{" "}
                      {formatFileSize(source.file_size)} &middot;{" "}
                      {source.media_type}
                    </span>
                  </div>
                  <button
                    className="btn btn-danger btn-small"
                    onClick={() => handleDelete(source.id)}
                  >
                    Delete
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
        <div className="editor-panel transcript-panel">
          <h2>Transcript</h2>
          <p className="placeholder-text">
            {sources.length > 0
              ? "Transcript will appear here after processing."
              : "Import media to get started."}
          </p>
        </div>
        <div className="editor-panel timeline-panel">
          <h2>Timeline</h2>
          <p className="placeholder-text">
            {sources.length > 0
              ? "The timeline will appear here once media is added."
              : "The timeline will appear here once media is added."}
          </p>
        </div>
      </div>
    </div>
  );
}
