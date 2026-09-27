import { useQuery } from '@tanstack/react-query';
import { getProgressSummary } from '../api/auth';
import { useAuthStore } from '../stores/authStore';

const BELT_COLORS: Record<string, string> = {
  white: 'bg-white text-gray-900',
  yellow: 'bg-yellow-400 text-gray-900',
  orange: 'bg-orange-500 text-white',
  green: 'bg-green-500 text-white',
  blue: 'bg-blue-500 text-white',
  purple: 'bg-purple-500 text-white',
  brown: 'bg-amber-800 text-white',
  black: 'bg-gray-900 text-white border border-gray-600',
};

export default function Profile() {
  const user = useAuthStore((s) => s.user);
  const { data: progress } = useQuery({
    queryKey: ['progress'],
    queryFn: getProgressSummary,
  });

  if (!user || !progress) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-12">
        <div className="animate-pulse space-y-4">
          <div className="h-32 bg-gray-800 rounded-xl" />
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Your Profile</h1>

      {/* Belt & XP */}
      <div className="bg-gray-800/50 border border-gray-700/50 rounded-xl p-6 mb-6 text-center">
        <div
          className={`inline-block px-6 py-2 rounded-full text-lg font-bold mb-3 ${
            BELT_COLORS[progress.current_belt]
          }`}
        >
          {progress.current_belt_display}
        </div>
        <p className="text-3xl font-bold text-primary-400 mb-1">{progress.total_xp} XP</p>
        {progress.next_belt_xp && (
          <>
            <p className="text-sm text-gray-400 mb-3">
              {progress.next_belt_xp - progress.total_xp} XP to next belt
            </p>
            <div className="bg-gray-700 rounded-full h-3 max-w-xs mx-auto">
              <div
                className="bg-primary-500 h-3 rounded-full transition-all"
                style={{
                  width: `${Math.min((progress.total_xp / progress.next_belt_xp) * 100, 100)}%`,
                }}
              />
            </div>
          </>
        )}
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <StatCard label="Modules Completed" value={`${progress.modules_completed}/${progress.modules_total}`} />
        <StatCard label="Exercises Completed" value={`${progress.exercises_completed}/${progress.exercises_total}`} />
        <StatCard label="Current Streak" value={`${progress.current_streak} days`} icon="🔥" />
        <StatCard label="Longest Streak" value={`${progress.longest_streak} days`} icon="⭐" />
      </div>

      {/* Account Info */}
      <div className="bg-gray-800/50 border border-gray-700/50 rounded-xl p-6">
        <h2 className="text-lg font-semibold mb-4">Account</h2>
        <div className="space-y-3 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-400">Username</span>
            <span>{user.username}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Email</span>
            <span>{user.email}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Member since</span>
            <span>{new Date(user.created_at).toLocaleDateString()}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ label, value, icon }: { label: string; value: string; icon?: string }) {
  return (
    <div className="bg-gray-800/50 border border-gray-700/50 rounded-xl p-4">
      <p className="text-sm text-gray-400 mb-1">{label}</p>
      <p className="text-xl font-bold">
        {icon && <span className="mr-1">{icon}</span>}
        {value}
      </p>
    </div>
  );
}
