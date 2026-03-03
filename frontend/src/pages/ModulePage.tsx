import { useQuery } from '@tanstack/react-query';
import { Link, useParams } from 'react-router-dom';
import { getModule } from '../api/curriculum';
import type { Lesson } from '../api/types';

const LESSON_TYPE_ICONS: Record<string, string> = {
  concept: '📖',
  interactive: '🧪',
  exercise: '✏️',
};

const LESSON_TYPE_LABELS: Record<string, string> = {
  concept: 'Concept',
  interactive: 'Interactive',
  exercise: 'Exercises',
};

export default function ModulePage() {
  const { moduleSlug } = useParams<{ moduleSlug: string }>();

  const { data: module, isLoading } = useQuery({
    queryKey: ['module', moduleSlug],
    queryFn: () => getModule(moduleSlug!),
    enabled: !!moduleSlug,
  });

  if (isLoading || !module) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-12">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-800 rounded w-64" />
          <div className="h-4 bg-gray-800 rounded w-96" />
          {[...Array(3)].map((_, i) => (
            <div key={i} className="h-20 bg-gray-800 rounded-xl" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <Link
        to="/dashboard"
        className="text-gray-400 hover:text-white text-sm mb-4 inline-flex items-center gap-1 transition-colors"
      >
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        Back to Learning Path
      </Link>

      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">{module.title}</h1>
        <p className="text-gray-400">{module.description}</p>
      </div>

      <div className="space-y-3">
        {module.lessons.map((lesson, index) => (
          <LessonCard
            key={lesson.id}
            lesson={lesson}
            moduleSlug={moduleSlug!}
            index={index}
          />
        ))}
      </div>

      {/* Module Complete Banner */}
      {module.is_completed && (
        <div className="mt-8 rounded-xl border border-primary-700/50 bg-primary-500/5 p-6 text-center">
          <div className="text-3xl mb-2">🎉</div>
          <h2 className="text-xl font-bold text-white mb-1">Module Complete!</h2>
          <p className="text-gray-400 text-sm mb-4">
            You've finished everything in <span className="text-white font-medium">{module.title}</span>.
          </p>
          {module.next_module ? (
            <Link
              to={`/module/${module.next_module.slug}`}
              className="inline-block bg-primary-600 hover:bg-primary-700 text-white px-8 py-3 rounded-xl font-medium transition-colors"
            >
              Continue to {module.next_module.title} →
            </Link>
          ) : (
            <Link
              to="/dashboard"
              className="inline-block bg-primary-600 hover:bg-primary-700 text-white px-8 py-3 rounded-xl font-medium transition-colors"
            >
              Back to Learning Path
            </Link>
          )}
        </div>
      )}
    </div>
  );
}

function LessonCard({
  lesson,
  moduleSlug,
  index,
}: {
  lesson: Lesson;
  moduleSlug: string;
  index: number;
}) {
  return (
    <Link
      to={`/module/${moduleSlug}/lesson/${lesson.slug}`}
      className={`block rounded-xl border px-6 py-4 transition-all ${
        lesson.is_completed
          ? 'bg-gray-800/40 border-primary-800/50'
          : 'bg-gray-800/50 border-gray-700/50 hover:border-primary-600/50'
      }`}
    >
      <div className="flex items-center gap-4">
        <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-gray-700/50 flex items-center justify-center text-lg">
          {lesson.is_completed ? '✅' : LESSON_TYPE_ICONS[lesson.lesson_type] || '📖'}
        </div>
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-0.5">
            <span className="text-xs text-gray-500 uppercase font-medium">
              {LESSON_TYPE_LABELS[lesson.lesson_type]}
            </span>
            <span className="text-xs text-gray-600">
              Step {index + 1}
            </span>
          </div>
          <h3 className="font-semibold text-white">{lesson.title}</h3>
        </div>
        <svg className="w-5 h-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
        </svg>
      </div>
    </Link>
  );
}
