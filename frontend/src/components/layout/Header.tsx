import { Link } from 'react-router-dom';
import { useAuthStore } from '../../stores/authStore';

const BELT_COLORS: Record<string, string> = {
  white: 'bg-white',
  yellow: 'bg-yellow-400',
  orange: 'bg-orange-500',
  green: 'bg-green-500',
  blue: 'bg-blue-500',
  purple: 'bg-purple-500',
  brown: 'bg-amber-800',
  black: 'bg-gray-900 border border-gray-600',
};

export default function Header() {
  const { user, isAuthenticated, logout } = useAuthStore();

  return (
    <header className="border-b border-gray-800 bg-gray-900/80 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2">
          <span className="text-2xl">🐍</span>
          <span className="text-xl font-bold text-white">
            Py<span className="text-primary-400">Starter</span>
          </span>
        </Link>

        <nav className="flex items-center gap-6">
          {isAuthenticated ? (
            <>
              <Link
                to="/dashboard"
                className="text-gray-300 hover:text-white transition-colors"
              >
                Learn
              </Link>
              <Link
                to="/profile"
                className="flex items-center gap-2 text-gray-300 hover:text-white transition-colors"
              >
                {user && (
                  <>
                    <div
                      className={`w-3 h-3 rounded-full ${BELT_COLORS[user.current_belt] || 'bg-white'}`}
                    />
                    <span className="text-primary-400 font-medium">
                      {user.total_xp} XP
                    </span>
                  </>
                )}
                <span>{user?.username}</span>
              </Link>
              <button
                onClick={logout}
                className="text-gray-400 hover:text-gray-200 text-sm transition-colors"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="text-gray-300 hover:text-white transition-colors"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
              >
                Get Started
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
