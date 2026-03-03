import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { getModules } from '../api/curriculum';
import { getProgressSummary } from '../api/auth';
import type { Module } from '../api/types';

const BELT_COLORS: Record<string, string> = {
  white: 'bg-white',
  yellow: 'bg-yellow-400',
  orange: 'bg-orange-500',
  green: 'bg-green-500',
  blue: 'bg-blue-500',
  purple: 'bg-purple-500',
  brown: 'bg-amber-800',
  black: 'bg-gray-900',
};

const MODULE_ICONS: Record<string, string> = {
  rocket: '🚀',
  box: '📦',
  'git-branch': '🔀',
  repeat: '🔁',
  code: '⚡',
  list: '📋',
  'book-open': '📖',
  type: '✨',
  wand: '🪄',
  network: '🌐',
};

export default function Dashboard() {
  const { data: modules, isLoading: modulesLoading } = useQuery({
    queryKey: ['modules'],
    queryFn: getModules,
  });
  const { data: progress } = useQuery({
    queryKey: ['progress'],
    queryFn: getProgressSummary,
  });

  if (modulesLoading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="animate-pulse space-y-4">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-24 bg-gray-800 rounded-xl" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Progress Header */}
      {progress && (
        <div className="bg-gray-800/50 border border-gray-700/50 rounded-xl p-6 mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold mb-1">Your Learning Path</h2>
              <p className="text-gray-400">
                {progress.modules_completed}/{progress.modules_total} modules completed
              </p>
            </div>
            <div className="text-right">
              <div className="flex items-center gap-2 mb-1">
                <div className={`w-4 h-4 rounded-full ${BELT_COLORS[progress.current_belt]}`} />
                <span className="font-semibold">{progress.current_belt_display}</span>
              </div>
              <p className="text-primary-400 font-bold text-lg">{progress.total_xp} XP</p>
              {progress.next_belt_xp && (
                <p className="text-xs text-gray-500">
                  {progress.next_belt_xp - progress.total_xp} XP to next belt
                </p>
              )}
            </div>
          </div>
          {/* XP Progress Bar */}
          {progress.next_belt_xp && (
            <div className="mt-4 bg-gray-700 rounded-full h-2">
              <div
                className="bg-primary-500 h-2 rounded-full transition-all duration-500"
                style={{
                  width: `${Math.min((progress.total_xp / progress.next_belt_xp) * 100, 100)}%`,
                }}
              />
            </div>
          )}
          {progress.current_streak > 0 && (
            <p className="text-sm text-gray-400 mt-3">
              🔥 {progress.current_streak} day streak
            </p>
          )}
        </div>
      )}

      {/* Module List */}
      <div className="space-y-3">
        {modules?.map((module, index) => (
          <ModuleCard key={module.id} module={module} index={index} />
        ))}
      </div>
    </div>
  );
}

function ModuleCard({ module, index }: { module: Module; index: number }) {
  const isLocked = !module.is_unlocked;

  return (
    <div
      className={`rounded-xl border transition-all ${
        isLocked
          ? 'bg-gray-800/30 border-gray-800 opacity-60'
          : module.is_completed
          ? 'bg-gray-800/50 border-primary-800/50'
          : 'bg-gray-800/50 border-gray-700/50 hover:border-primary-600/50'
      }`}
    >
      {isLocked ? (
        <div className="flex items-center gap-5 px-6 py-5">
          <div className="flex-shrink-0 w-12 h-12 rounded-xl bg-gray-700/50 flex items-center justify-center text-xl">
            🔒
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-500 font-medium">Module {index + 1}</span>
            </div>
            <h3 className="text-lg font-semibold text-gray-500">{module.title}</h3>
            <p className="text-sm text-gray-600">{module.description}</p>
          </div>
        </div>
      ) : (
        <Link to={`/module/${module.slug}`} className="flex items-center gap-5 px-6 py-5">
          <div className="flex-shrink-0 w-12 h-12 rounded-xl bg-gray-700/50 flex items-center justify-center text-xl">
            {module.is_completed ? '✅' : MODULE_ICONS[module.icon] || '📘'}
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-400 font-medium">Module {index + 1}</span>
              {module.is_completed && (
                <span className="text-xs bg-primary-600/20 text-primary-400 px-2 py-0.5 rounded-full">
                  Completed
                </span>
              )}
            </div>
            <h3 className="text-lg font-semibold text-white">{module.title}</h3>
            <p className="text-sm text-gray-400">{module.description}</p>
            {!module.is_completed && module.progress_percent > 0 && (
              <div className="mt-2 bg-gray-700 rounded-full h-1.5 w-48">
                <div
                  className="bg-primary-500 h-1.5 rounded-full"
                  style={{ width: `${module.progress_percent}%` }}
                />
              </div>
            )}
          </div>
          <div className="text-gray-500">
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </div>
        </Link>
      )}
    </div>
  );
}
