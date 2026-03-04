import { useState, useCallback } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { Link, useParams, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { getExercise, getLesson, getModule, revealHint, getRevealedHints } from '../api/curriculum';
import { runCode, submitCode, getAiHint, getAiCritique, explainError } from '../api/submissions';
import { useAuthStore } from '../stores/authStore';
import CodeEditor from '../components/editor/CodeEditor';
import type { Hint, Submission } from '../api/types';

export default function ExercisePage() {
  const { moduleSlug, lessonSlug, exerciseSlug } = useParams<{
    moduleSlug: string;
    lessonSlug: string;
    exerciseSlug: string;
  }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const loadUser = useAuthStore((s) => s.loadUser);

  const { data: exercise, isLoading } = useQuery({
    queryKey: ['exercise', moduleSlug, lessonSlug, exerciseSlug],
    queryFn: () => getExercise(moduleSlug!, lessonSlug!, exerciseSlug!),
    enabled: !!moduleSlug && !!lessonSlug && !!exerciseSlug,
  });

  const { data: lesson } = useQuery({
    queryKey: ['lesson', moduleSlug, lessonSlug],
    queryFn: () => getLesson(moduleSlug!, lessonSlug!),
    enabled: !!moduleSlug && !!lessonSlug,
  });

  const { data: module } = useQuery({
    queryKey: ['module', moduleSlug],
    queryFn: () => getModule(moduleSlug!),
    enabled: !!moduleSlug,
  });

  const [code, setCode] = useState('');
  const [result, setResult] = useState<Submission | null>(null);
  const [running, setRunning] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [hints, setHints] = useState<Hint[]>([]);
  const [aiHint, setAiHint] = useState('');
  const [aiCritique, setAiCritique] = useState('');
  const [aiExplanation, setAiExplanation] = useState('');
  const [aiLoading, setAiLoading] = useState(false);
  const [selectedChoice, setSelectedChoice] = useState<number | null>(null);
  const [choiceResult, setChoiceResult] = useState<'correct' | 'wrong' | null>(null);

  // Initialize code when exercise loads
  const [codeInitialized, setCodeInitialized] = useState('');
  if (exercise && exercise.slug !== codeInitialized) {
    setCode(exercise.starter_code);
    setCodeInitialized(exercise.slug);
    setResult(null);
    setHints([]);
    setAiHint('');
    setAiCritique('');
    setAiExplanation('');
    setSelectedChoice(null);
    setChoiceResult(null);
  }

  // Load revealed hints
  useQuery({
    queryKey: ['hints', exercise?.id],
    queryFn: () => getRevealedHints(exercise!.id),
    enabled: !!exercise?.id,
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    onSuccess: (data: any) => setHints(data),
  } as any);

  const handleRun = useCallback(async () => {
    if (!exercise) return;
    setRunning(true);
    setResult(null);
    setAiExplanation('');
    try {
      const res = await runCode(exercise.id, code);
      setResult(res);
    } catch {
      setResult(null);
    } finally {
      setRunning(false);
    }
  }, [exercise, code]);

  const handleSubmit = useCallback(async () => {
    if (!exercise) return;
    setSubmitting(true);
    setResult(null);
    setAiExplanation('');
    setAiCritique('');
    try {
      const res = await submitCode(exercise.id, code);
      setResult(res);
      if (res.status === 'passed') {
        queryClient.invalidateQueries({ queryKey: ['exercise'] });
        queryClient.invalidateQueries({ queryKey: ['lesson'] });
        queryClient.invalidateQueries({ queryKey: ['module'] });
        queryClient.invalidateQueries({ queryKey: ['modules'] });
        queryClient.invalidateQueries({ queryKey: ['progress'] });
        loadUser(); // Refresh user XP in header
      }
    } catch {
      setResult(null);
    } finally {
      setSubmitting(false);
    }
  }, [exercise, code, queryClient]);

  const handleRevealHint = useCallback(async () => {
    if (!exercise) return;
    try {
      const hint = await revealHint(exercise.id);
      setHints((prev) => [...prev, hint]);
    } catch {
      // No more hints
    }
  }, [exercise]);

  const handleAiHint = useCallback(async () => {
    if (!exercise) return;
    setAiLoading(true);
    try {
      const lastError = result?.error_message || '';
      const res = await getAiHint(exercise.id, code, lastError);
      setAiHint(res.hint);
    } catch {
      setAiHint('Sorry, could not get AI help right now.');
    } finally {
      setAiLoading(false);
    }
  }, [exercise, code, result]);

  const handleAiCritique = useCallback(async () => {
    if (!exercise) return;
    setAiLoading(true);
    try {
      const res = await getAiCritique(exercise.id, code);
      setAiCritique(res.feedback);
    } catch {
      setAiCritique('Sorry, could not get feedback right now.');
    } finally {
      setAiLoading(false);
    }
  }, [exercise, code]);

  const handleExplainError = useCallback(async () => {
    if (!exercise || !result?.error_message) return;
    setAiLoading(true);
    try {
      const res = await explainError(exercise.id, code, result.error_message);
      setAiExplanation(res.explanation);
    } catch {
      setAiExplanation('Sorry, could not explain the error right now.');
    } finally {
      setAiLoading(false);
    }
  }, [exercise, code, result]);

  const handleChoiceSubmit = useCallback(() => {
    if (!exercise?.choices || selectedChoice === null) return;
    const choice = exercise.choices[selectedChoice];
    setChoiceResult(choice.is_correct ? 'correct' : 'wrong');
    if (choice.is_correct) {
      // Submit as correct
      submitCode(exercise.id, `# Answer: ${choice.label}`).then((res) => {
        setResult(res);
        queryClient.invalidateQueries({ queryKey: ['exercise'] });
        queryClient.invalidateQueries({ queryKey: ['module'] });
        queryClient.invalidateQueries({ queryKey: ['modules'] });
        queryClient.invalidateQueries({ queryKey: ['progress'] });
        loadUser();
      });
    }
  }, [exercise, selectedChoice, queryClient]);

  if (isLoading || !exercise) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-12">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-800 rounded w-64" />
          <div className="h-64 bg-gray-800 rounded-xl" />
        </div>
      </div>
    );
  }

  const isPassed = result?.status === 'passed' || exercise.is_completed;

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <Link
        to={`/module/${moduleSlug}/lesson/${lessonSlug}`}
        className="text-gray-400 hover:text-white text-sm mb-4 inline-flex items-center gap-1 transition-colors"
      >
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        Back to Lesson
      </Link>

      <div className="flex items-center gap-3 mb-4">
        <h1 className="text-2xl font-bold">{exercise.title}</h1>
        <span className="text-xs bg-gray-700 text-gray-300 px-2 py-1 rounded uppercase">
          {exercise.exercise_type.replace('_', ' ')}
        </span>
        <span className="text-xs text-primary-400 font-medium">{exercise.xp_value} XP</span>
      </div>

      {/* Instructions */}
      <div className="lesson-content bg-gray-800/50 border border-gray-700/50 rounded-xl p-6 mb-6">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{exercise.instructions}</ReactMarkdown>
      </div>

      {/* Output Predict Exercise */}
      {exercise.exercise_type === 'output_predict' && exercise.choices ? (
        <div className="mb-6">
          <div className="space-y-2">
            {exercise.choices.map((choice, i) => (
              <button
                key={i}
                onClick={() => {
                  setSelectedChoice(i);
                  setChoiceResult(null);
                }}
                className={`w-full text-left px-5 py-3 rounded-lg border transition-all ${
                  selectedChoice === i
                    ? choiceResult === 'correct'
                      ? 'border-green-500 bg-green-500/10'
                      : choiceResult === 'wrong'
                      ? 'border-red-500 bg-red-500/10'
                      : 'border-primary-500 bg-primary-500/10'
                    : 'border-gray-700 bg-gray-800/50 hover:border-gray-600'
                }`}
              >
                <code className="font-mono">{choice.label}</code>
              </button>
            ))}
          </div>
          {choiceResult === 'wrong' && (
            <p className="text-red-400 text-sm mt-3">Not quite! Try again.</p>
          )}
          {choiceResult === 'correct' && (
            <p className="text-green-400 text-sm mt-3">Correct! Great job!</p>
          )}
          <button
            onClick={handleChoiceSubmit}
            disabled={selectedChoice === null || choiceResult === 'correct'}
            className="mt-4 bg-primary-600 hover:bg-primary-700 disabled:opacity-50 text-white px-6 py-2.5 rounded-lg font-medium transition-colors"
          >
            Check Answer
          </button>
        </div>
      ) : (
        /* Code Editor Exercise */
        <>
          <div className="border border-gray-700 rounded-xl overflow-hidden mb-4">
            <div className="bg-gray-800 px-4 py-2 border-b border-gray-700 flex items-center justify-between">
              <span className="text-sm text-gray-400 font-mono">solution.py</span>
              <div className="flex gap-2">
                <button
                  onClick={handleRun}
                  disabled={running || submitting}
                  className="bg-gray-700 hover:bg-gray-600 disabled:opacity-50 text-white px-4 py-1.5 rounded-md text-sm font-medium transition-colors"
                >
                  {running ? 'Running...' : '▶ Run'}
                </button>
                <button
                  onClick={handleSubmit}
                  disabled={running || submitting}
                  className="bg-primary-600 hover:bg-primary-700 disabled:opacity-50 text-white px-4 py-1.5 rounded-md text-sm font-medium transition-colors"
                >
                  {submitting ? 'Submitting...' : '✓ Submit'}
                </button>
              </div>
            </div>
            <CodeEditor value={code} onChange={setCode} height="250px" />
          </div>

          {/* Test Results */}
          {result && (
            <div
              className={`rounded-xl border p-5 mb-4 ${
                result.status === 'passed'
                  ? 'border-green-700/50 bg-green-500/5'
                  : 'border-red-700/50 bg-red-500/5'
              }`}
            >
              <div className="flex items-center gap-2 mb-3">
                <span className="text-lg">{result.status === 'passed' ? '🎉' : '❌'}</span>
                <h3 className="font-semibold">
                  {result.status === 'passed'
                    ? result.is_run_only
                      ? 'Tests Passed!'
                      : `Exercise Complete! +${result.xp_awarded} XP`
                    : `${result.passed_tests}/${result.total_tests} tests passed`}
                </h3>
              </div>

              {result.error_message && (
                <div className="bg-gray-900 rounded-lg p-3 mb-3">
                  <pre className="text-sm text-red-400 font-mono whitespace-pre-wrap">
                    {result.error_message}
                  </pre>
                  <button
                    onClick={handleExplainError}
                    disabled={aiLoading}
                    className="mt-2 text-xs text-primary-400 hover:text-primary-300 transition-colors"
                  >
                    {aiLoading ? 'Explaining...' : '🤖 Explain this error'}
                  </button>
                </div>
              )}

              {result.test_results
                .filter((r) => !r.is_hidden)
                .map((tr) => (
                  <div
                    key={tr.id}
                    className={`flex items-start gap-2 py-2 text-sm ${
                      tr.passed ? 'text-green-400' : 'text-red-400'
                    }`}
                  >
                    <span>{tr.passed ? '✓' : '✗'}</span>
                    <div>
                      <p>{tr.description || (tr.passed ? 'Passed' : 'Failed')}</p>
                      {!tr.passed && (
                        <div className="mt-1 text-xs font-mono text-gray-400">
                          <p>
                            Expected: <span className="text-green-400">{tr.expected_output}</span>
                          </p>
                          <p>
                            Got: <span className="text-red-400">{tr.actual_output || '(no output)'}</span>
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                ))}

              {/* AI Critique (on success) */}
              {result.status === 'passed' && !result.is_run_only && !aiCritique && (
                <button
                  onClick={handleAiCritique}
                  disabled={aiLoading}
                  className="mt-3 text-sm text-primary-400 hover:text-primary-300 transition-colors"
                >
                  {aiLoading ? 'Getting feedback...' : '🤖 Get AI feedback on your code'}
                </button>
              )}
            </div>
          )}
        </>
      )}

      {/* AI Explanation */}
      {aiExplanation && (
        <div className="bg-blue-500/5 border border-blue-700/50 rounded-xl p-5 mb-4">
          <h3 className="font-semibold text-blue-400 mb-2">🤖 Error Explanation</h3>
          <div className="text-sm text-gray-300 lesson-content">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{aiExplanation}</ReactMarkdown>
          </div>
        </div>
      )}

      {/* AI Critique */}
      {aiCritique && (
        <div className="bg-primary-500/5 border border-primary-700/50 rounded-xl p-5 mb-4">
          <h3 className="font-semibold text-primary-400 mb-2">🤖 Code Feedback</h3>
          <div className="text-sm text-gray-300 lesson-content">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{aiCritique}</ReactMarkdown>
          </div>
        </div>
      )}

      {/* Hints Section */}
      <div className="mt-6">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-semibold text-gray-300">Hints</h3>
          <div className="flex gap-2">
            {hints.length < exercise.hints_available && (
              <button
                onClick={handleRevealHint}
                className="text-sm text-yellow-400 hover:text-yellow-300 transition-colors"
              >
                💡 Reveal Hint ({hints.length}/{exercise.hints_available})
              </button>
            )}
            <button
              onClick={handleAiHint}
              disabled={aiLoading}
              className="text-sm text-primary-400 hover:text-primary-300 transition-colors"
            >
              {aiLoading ? 'Thinking...' : '🤖 Ask AI for Help'}
            </button>
          </div>
        </div>

        {hints.map((hint) => (
          <div
            key={hint.id}
            className="bg-yellow-500/5 border border-yellow-700/30 rounded-lg p-4 mb-2"
          >
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-medium text-yellow-400">{hint.level_name}</span>
              {hint.xp_penalty_percent > 0 && (
                <span className="text-xs text-gray-500">
                  (-{hint.xp_penalty_percent}% XP)
                </span>
              )}
            </div>
            <div className="text-sm text-gray-300 lesson-content">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{hint.content}</ReactMarkdown>
            </div>
          </div>
        ))}

        {aiHint && (
          <div className="bg-primary-500/5 border border-primary-700/30 rounded-lg p-4 mb-2">
            <span className="text-xs font-medium text-primary-400">🤖 AI Hint</span>
            <div className="text-sm text-gray-300 mt-1 lesson-content">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{aiHint}</ReactMarkdown>
            </div>
          </div>
        )}
      </div>

      {/* Next Exercise / Next Module / Back to Lesson */}
      {isPassed && (() => {
        // Check if all exercises in this lesson are now done
        const allLessonExercisesDone = lesson?.exercises?.length
          ? lesson.exercises.every((ex) =>
              ex.slug === exerciseSlug ? true : ex.is_completed
            )
          : false;
        const moduleComplete = allLessonExercisesDone && module?.is_completed;
        const nextModule = module?.next_module;

        // Find next incomplete exercise in this lesson
        const nextExercise = lesson?.exercises?.find(
          (ex) => !ex.is_completed && ex.slug !== exerciseSlug
        );

        return (
          <div className="mt-8 text-center space-y-3">
            {moduleComplete && nextModule ? (
              <>
                <p className="text-primary-400 font-medium">
                  Module complete! Nice work!
                </p>
                <Link
                  to={`/module/${nextModule.slug}`}
                  className="inline-block bg-primary-600 hover:bg-primary-700 text-white px-8 py-3 rounded-xl font-medium transition-colors"
                >
                  Continue to {nextModule.title} →
                </Link>
              </>
            ) : nextExercise ? (
              <Link
                to={`/module/${moduleSlug}/lesson/${lessonSlug}/exercise/${nextExercise.slug}`}
                className="inline-block bg-primary-600 hover:bg-primary-700 text-white px-8 py-3 rounded-xl font-medium transition-colors"
              >
                Next Exercise →
              </Link>
            ) : (
              <button
                onClick={() => navigate(`/module/${moduleSlug}/lesson/${lessonSlug}`)}
                className="bg-primary-600 hover:bg-primary-700 text-white px-8 py-3 rounded-xl font-medium transition-colors"
              >
                Continue →
              </button>
            )}
          </div>
        );
      })()}
    </div>
  );
}
