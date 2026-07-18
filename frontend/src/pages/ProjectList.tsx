import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { listProjects, createProject, deleteProject } from "../api/projects";
import type { Project } from "../api/projects";

export default function ProjectList() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [newName, setNewName] = useState("");
  const [newDescription, setNewDescription] = useState("");

  const fetchProjects = useCallback(async () => {
    try {
      const data = await listProjects();
      setProjects(data);
    } catch (err) {
      console.error("Failed to load projects", err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchProjects();
  }, [fetchProjects]);

  const handleCreate = async () => {
    if (!newName.trim()) return;
    try {
      const project = await createProject({
        name: newName.trim(),
        description: newDescription.trim() || undefined,
      });
      setProjects((prev) => [project, ...prev]);
      setShowCreate(false);
      setNewName("");
      setNewDescription("");
    } catch (err) {
      console.error("Failed to create project", err);
    }
  };

  const handleDelete = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm("Delete this project?")) return;
    try {
      await deleteProject(id);
      setProjects((prev) => prev.filter((p) => p.id !== id));
    } catch (err) {
      console.error("Failed to delete project", err);
    }
  };

  if (loading) return <div className="loading">Loading projects...</div>;

  return (
    <div className="project-list">
      <header className="project-list-header">
        <h1>Projects</h1>
        <button className="btn btn-primary" onClick={() => setShowCreate(true)}>
          New Project
        </button>
      </header>

      {showCreate && (
        <div className="create-form">
          <input
            type="text"
            placeholder="Project name"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            autoFocus
          />
          <input
            type="text"
            placeholder="Description (optional)"
            value={newDescription}
            onChange={(e) => setNewDescription(e.target.value)}
          />
          <div className="form-actions">
            <button className="btn btn-primary" onClick={handleCreate}>
              Create
            </button>
            <button className="btn btn-secondary" onClick={() => setShowCreate(false)}>
              Cancel
            </button>
          </div>
        </div>
      )}

      {projects.length === 0 ? (
        <p className="empty-state">No projects yet. Click "New Project" to get started.</p>
      ) : (
        <ul className="projects">
          {projects.map((project) => (
            <li
              key={project.id}
              className="project-card"
              onClick={() => navigate(`/projects/${project.id}`)}
            >
              <div className="project-card-body">
                <h3>{project.name}</h3>
                {project.description && <p>{project.description}</p>}
                <span className="project-date">
                  Created {new Date(project.created_at).toLocaleDateString()}
                </span>
              </div>
              <button
                className="btn btn-danger"
                onClick={(e) => handleDelete(project.id, e)}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
