import { useState, useCallback } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { Link, useParams, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { getLesson, getModule, markLessonComplete } from '../api/curriculum';
import { sandboxRun } from '../api/submissions';
import CodeEditor from '../components/editor/CodeEditor';

export default function LessonPage() {
  const { moduleSlug, lessonSlug } = useParams<{
    moduleSlug: string;
    lessonSlug: string;
  }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: lesson, isLoading } = useQuery({
    queryKey: ['lesson', moduleSlug, lessonSlug],
    queryFn: () => getLesson(moduleSlug!, lessonSlug!),
    enabled: !!moduleSlug && !!lessonSlug,
  });

  const { data: module } = useQuery({
    queryKey: ['module', moduleSlug],
    queryFn: () => getModule(moduleSlug!),
    enabled: !!moduleSlug,
  });

  const [sandboxCode, setSandboxCode] = useState('');
  const [sandboxOutput, setSandboxOutput] = useState('');
  const [running, setRunning] = useState(false);

  // Initialize sandbox code when lesson loads
  const [initialized, setInitialized] = useState(false);
  if (lesson?.sandbox_code && !initialized) {
    setSandboxCode(lesson.sandbox_code);
    setInitialized(true);
  }

  const handleRunSandbox = useCallback(async () => {
    if (!sandboxCode.trim()) return;
    setRunning(true);
    setSandboxOutput('');
    try {
      const result = await sandboxRun(sandboxCode);
      if (result.error) {
        setSandboxOutput(result.error);
      } else {
        setSandboxOutput(result.output || '(no output)');
      }
    } catch {
      setSandboxOutput('Something went wrong. Please try again.');
    } finally {
      setRunning(false);
    }
  }, [sandboxCode]);

  const handleMarkComplete = async () => {
    if (!lesson) return;
    try {
      await markLessonComplete(lesson.id);
      queryClient.invalidateQueries({ queryKey: ['lesson'] });
      queryClient.invalidateQueries({ queryKey: ['module'] });
      queryClient.invalidateQueries({ queryKey: ['modules'] });
      queryClient.invalidateQueries({ queryKey: ['progress'] });
      navigate(`/module/${moduleSlug}`);
    } catch {
      // Silently handle - might already be completed
      navigate(`/module/${moduleSlug}`);
    }
  };

  if (isLoading || !lesson) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-12">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-800 rounded w-64" />
          <div className="h-4 bg-gray-800 rounded w-full" />
          <div className="h-4 bg-gray-800 rounded w-3/4" />
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <Link
        to={`/module/${moduleSlug}`}
        className="text-gray-400 hover:text-white text-sm mb-4 inline-flex items-center gap-1 transition-colors"
      >
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        Back to Module
      </Link>

      {/* Lesson Content */}
      <div className="lesson-content mb-8">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{lesson.content}</ReactMarkdown>
      </div>

      {/* Interactive Sandbox */}
      {lesson.lesson_type === 'interactive' && (
        <div className="mb-8 border border-gray-700 rounded-xl overflow-hidden">
          <div className="bg-gray-800 px-4 py-2 border-b border-gray-700 flex items-center justify-between">
            <span className="text-sm text-gray-400">🧪 Try it yourself</span>
            <button
              onClick={handleRunSandbox}
              disabled={running}
              className="bg-primary-600 hover:bg-primary-700 disabled:opacity-50 text-white px-4 py-1.5 rounded-md text-sm font-medium transition-colors"
            >
              {running ? 'Running...' : '▶ Run'}
            </button>
          </div>
          <CodeEditor value={sandboxCode} onChange={setSandboxCode} height="200px" />
          {sandboxOutput && (
            <div className="bg-gray-900 border-t border-gray-700 p-4">
              <p className="text-xs text-gray-500 mb-1">Output:</p>
              <pre className="text-sm text-green-400 font-mono whitespace-pre-wrap">
                {sandboxOutput}
              </pre>
            </div>
          )}
        </div>
      )}

      {/* Exercise Links */}
      {lesson.lesson_type === 'exercise' && lesson.exercises.length > 0 && (
        <div className="space-y-3 mb-8">
          <h3 className="text-lg font-semibold">Exercises</h3>
          {lesson.exercises.map((ex) => (
            <Link
              key={ex.id}
              to={`/module/${moduleSlug}/lesson/${lessonSlug}/exercise/${ex.slug}`}
              className={`block rounded-lg border px-5 py-4 transition-all ${
                ex.is_completed
                  ? 'bg-gray-800/40 border-primary-800/50'
                  : 'bg-gray-800/50 border-gray-700/50 hover:border-primary-600/50'
              }`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2 mb-0.5">
                    <span className="text-xs text-gray-500 uppercase">
                      {ex.exercise_type.replace('_', ' ')}
                    </span>
                    <span className="text-xs text-primary-400">{ex.xp_value} XP</span>
                  </div>
                  <h4 className="font-medium text-white">{ex.title}</h4>
                </div>
                <span>{ex.is_completed ? '✅' : '→'}</span>
              </div>
            </Link>
          ))}

          {/* All exercises done — continue to next module */}
          {lesson.exercises.length > 0 &&
            lesson.exercises.every((ex) => ex.is_completed) &&
            module && (
              <div className="mt-4 rounded-xl border border-primary-700/50 bg-primary-500/5 p-5 text-center">
                <p className="text-primary-400 font-medium mb-3">
                  All exercises complete!
                </p>
                {module.is_completed && module.next_module ? (
                  <Link
                    to={`/module/${module.next_module.slug}`}
                    className="inline-block bg-primary-600 hover:bg-primary-700 text-white px-6 py-2.5 rounded-xl font-medium transition-colors"
                  >
                    Continue to {module.next_module.title} →
                  </Link>
                ) : (
                  <Link
                    to={`/module/${moduleSlug}`}
                    className="inline-block bg-primary-600 hover:bg-primary-700 text-white px-6 py-2.5 rounded-xl font-medium transition-colors"
                  >
                    Back to Module →
                  </Link>
                )}
              </div>
            )}
        </div>
      )}

      {/* Complete Button (for concept/interactive lessons) */}
      {lesson.lesson_type !== 'exercise' && !lesson.is_completed && (
        <button
          onClick={handleMarkComplete}
          className="w-full bg-primary-600 hover:bg-primary-700 text-white py-3 rounded-xl font-medium transition-colors"
        >
          Mark as Complete & Continue
        </button>
      )}

      {lesson.is_completed && lesson.lesson_type !== 'exercise' && (
        <div className="text-center text-primary-400 py-3">
          ✅ Lesson completed!
        </div>
      )}
    </div>
  );
}
