export interface User {
  id: number;
  username: string;
  email: string;
  bio: string;
  total_xp: number;
  current_belt: string;
  current_belt_display: string;
  next_belt_xp: number | null;
  current_streak: number;
  longest_streak: number;
  last_activity_date: string | null;
  created_at: string;
}

export interface ProgressSummary {
  total_xp: number;
  current_belt: string;
  current_belt_display: string;
  next_belt_xp: number | null;
  modules_completed: number;
  modules_total: number;
  exercises_completed: number;
  exercises_total: number;
  current_streak: number;
  longest_streak: number;
}

export interface Module {
  id: number;
  title: string;
  slug: string;
  description: string;
  order: number;
  icon: string;
  lesson_count: number;
  total_xp: number;
  is_unlocked: boolean;
  is_completed: boolean;
  progress_percent: number;
}

export interface ModuleDetail extends Module {
  lessons: Lesson[];
  next_module: { slug: string; title: string } | null;
}

export interface Lesson {
  id: number;
  title: string;
  slug: string;
  order: number;
  lesson_type: 'concept' | 'interactive' | 'exercise';
  exercise_count?: number;
  is_completed: boolean;
}

export interface LessonDetail extends Lesson {
  content: string;
  sandbox_code: string;
  exercises: Exercise[];
}

export interface Exercise {
  id: number;
  title: string;
  slug: string;
  order: number;
  exercise_type: 'fill_blank' | 'fix_bug' | 'write_code' | 'output_predict';
  difficulty: number;
  xp_value: number;
  concepts: string;
  is_completed: boolean;
}

export interface ExerciseDetail extends Exercise {
  instructions: string;
  starter_code: string;
  choices: { label: string; is_correct: boolean }[] | null;
  test_cases: TestCase[];
  hints_available: number;
  user_attempts: number;
}

export interface TestCase {
  id: number;
  input_data: string;
  expected_output: string;
  description: string;
  is_hidden: boolean;
}

export interface Hint {
  id: number;
  level: number;
  level_name: string;
  content: string;
  xp_penalty_percent: number;
}

export interface Submission {
  id: number;
  exercise: number;
  exercise_title: string;
  code: string;
  status: 'pending' | 'running' | 'passed' | 'failed' | 'error' | 'timeout';
  passed_tests: number;
  total_tests: number;
  execution_time: number | null;
  error_message: string;
  xp_awarded: number;
  is_run_only: boolean;
  test_results: TestCaseResult[];
  created_at: string;
}

export interface TestCaseResult {
  id: number;
  passed: boolean;
  actual_output: string;
  expected_output: string;
  error_message: string;
  execution_time: number | null;
  description: string;
  is_hidden: boolean;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}
