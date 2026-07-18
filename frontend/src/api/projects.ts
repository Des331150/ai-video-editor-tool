import { apiRequest } from "./client";

export interface Project {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreateProjectPayload {
  name: string;
  description?: string;
}

export async function listProjects(): Promise<Project[]> {
  return apiRequest<Project[]>("/api/projects");
}

export async function createProject(payload: CreateProjectPayload): Promise<Project> {
  return apiRequest<Project>("/api/projects", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getProject(id: string): Promise<Project> {
  return apiRequest<Project>(`/api/projects/${id}`);
}

export async function deleteProject(id: string): Promise<void> {
  return apiRequest<void>(`/api/projects/${id}`, {
    method: "DELETE",
  });
}
