import { apiRequest } from "./client";

export interface TranscriptEntry {
  word: string;
  start_time: number;
  end_time: number;
  position: number;
}

export interface Transcript {
  source_id: string;
  entries: TranscriptEntry[];
}

export async function getTranscript(
  projectId: string,
  sourceId: string
): Promise<Transcript> {
  return apiRequest<Transcript>(
    `/api/projects/${projectId}/sources/${sourceId}/transcript`
  );
}
