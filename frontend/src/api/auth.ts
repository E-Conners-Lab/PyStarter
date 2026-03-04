import client from './client';
import type { AuthTokens, ProgressSummary, User } from './types';

export async function login(username: string, password: string): Promise<AuthTokens> {
  const res = await client.post('/accounts/login/', { username, password });
  return res.data;
}

export async function register(
  username: string,
  password: string
): Promise<{ user: User; tokens: AuthTokens }> {
  const res = await client.post('/accounts/register/', { username, password });
  return res.data;
}

export async function getMe(): Promise<User> {
  const res = await client.get('/accounts/me/');
  return res.data;
}

export async function getProgressSummary(): Promise<ProgressSummary> {
  const res = await client.get('/accounts/progress/');
  return res.data;
}

export async function getLeaderboard(): Promise<
  { username: string; total_xp: number; current_belt: string; current_belt_display: string }[]
> {
  const res = await client.get('/accounts/leaderboard/');
  return res.data;
}
