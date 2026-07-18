import { apiRequest } from "./client";

export interface SourceMedia {
  id: string;
  project_id: string;
  filename: string;
  duration: number | null;
  file_size: number;
  media_type: string;
  created_at: string;
}

export async function listSources(projectId: string): Promise<SourceMedia[]> {
  return apiRequest<SourceMedia[]>(`/api/projects/${projectId}/sources`);
}

export async function uploadSource(
  projectId: string,
  file: File,
  duration?: number
): Promise<SourceMedia> {
  const formData = new FormData();
  formData.append("file", file);
  if (duration !== undefined) {
    formData.append("duration", String(duration));
  }
  return apiRequest<SourceMedia>(`/api/projects/${projectId}/sources`, {
    method: "POST",
    body: formData,
  });
}

export async function deleteSource(
  projectId: string,
  sourceId: string
): Promise<void> {
  return apiRequest<void>(
    `/api/projects/${projectId}/sources/${sourceId}`,
    { method: "DELETE" }
  );
}
