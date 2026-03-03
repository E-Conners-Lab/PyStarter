import client from './client';
import type { Submission } from './types';

export async function sandboxRun(code: string): Promise<{
  status: string;
  output: string;
  error: string;
  execution_time: number | null;
}> {
  const res = await client.post('/submissions/sandbox/', { code });
  return res.data;
}

export async function runCode(exerciseId: number, code: string): Promise<Submission> {
  const res = await client.post(`/submissions/run/${exerciseId}/`, { code });
  return res.data;
}

export async function submitCode(exerciseId: number, code: string): Promise<Submission> {
  const res = await client.post(`/submissions/submit/${exerciseId}/`, { code });
  return res.data;
}

export async function getSubmissionHistory(exerciseId: number): Promise<Submission[]> {
  const res = await client.get(`/submissions/history/${exerciseId}/`);
  return res.data;
}

export async function getAiHint(
  exerciseId: number,
  code: string,
  error?: string
): Promise<{ hint: string }> {
  const res = await client.post(`/ai/hint/${exerciseId}/`, { code, error });
  return res.data;
}

export async function getAiCritique(
  exerciseId: number,
  code: string
): Promise<{ feedback: string }> {
  const res = await client.post(`/ai/critique/${exerciseId}/`, { code });
  return res.data;
}

export async function explainError(
  exerciseId: number,
  code: string,
  error: string
): Promise<{ explanation: string }> {
  const res = await client.post(`/ai/explain-error/${exerciseId}/`, { code, error });
  return res.data;
}
