import client from './client';
import type { ExerciseDetail, Hint, LessonDetail, Module, ModuleDetail } from './types';

export async function getModules(): Promise<Module[]> {
  const res = await client.get('/curriculum/modules/');
  return res.data;
}

export async function getModule(slug: string): Promise<ModuleDetail> {
  const res = await client.get(`/curriculum/modules/${slug}/`);
  return res.data;
}

export async function getLesson(moduleSlug: string, lessonSlug: string): Promise<LessonDetail> {
  const res = await client.get(`/curriculum/modules/${moduleSlug}/lessons/${lessonSlug}/`);
  return res.data;
}

export async function getExercise(
  moduleSlug: string,
  lessonSlug: string,
  exerciseSlug: string
): Promise<ExerciseDetail> {
  const res = await client.get(
    `/curriculum/modules/${moduleSlug}/lessons/${lessonSlug}/exercises/${exerciseSlug}/`
  );
  return res.data;
}

export async function revealHint(exerciseId: number): Promise<Hint> {
  const res = await client.post(`/curriculum/exercises/${exerciseId}/hint/`);
  return res.data;
}

export async function getRevealedHints(exerciseId: number): Promise<Hint[]> {
  const res = await client.get(`/curriculum/exercises/${exerciseId}/hints/`);
  return res.data;
}

export async function markLessonComplete(lessonId: number): Promise<void> {
  await client.post(`/curriculum/lessons/${lessonId}/complete/`);
}
