import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getProject } from "../api/projects";
import type { Project } from "../api/projects";

export default function ProjectEditor() {
  const { projectId } = useParams<{ projectId: string }>();
  const navigate = useNavigate();
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);

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
        <div className="editor-panel transcript-panel">
          <h2>Transcript</h2>
          <p className="placeholder-text">No source media yet. Import media to get started.</p>
        </div>
        <div className="editor-panel timeline-panel">
          <h2>Timeline</h2>
          <p className="placeholder-text">The timeline will appear here once media is added.</p>
        </div>
      </div>
    </div>
  );
}
