import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';

export default function Register() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const register = useAuthStore((s) => s.register);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await register(username, email, password);
      navigate('/dashboard');
    } catch (err: unknown) {
      if (err && typeof err === 'object' && 'response' in err) {
        const axiosErr = err as { response?: { data?: Record<string, string[]> } };
        const data = axiosErr.response?.data;
        if (data) {
          const messages = Object.values(data).flat();
          setError(messages.join(' '));
        } else {
          setError('Registration failed. Please try again.');
        }
      } else {
        setError('Registration failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <h1 className="text-3xl font-bold text-center mb-2">Start Learning Python</h1>
        <p className="text-gray-400 text-center mb-8">Create your free account</p>
        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="bg-red-500/10 border border-red-500/30 text-red-400 px-4 py-3 rounded-lg text-sm">
              {error}
            </div>
          )}
          <div>
            <label htmlFor="reg-username" className="block text-sm text-gray-400 mb-1">Username</label>
            <input
              id="reg-username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:border-primary-500 focus:outline-none transition-colors"
              required
            />
          </div>
          <div>
            <label htmlFor="reg-email" className="block text-sm text-gray-400 mb-1">Email</label>
            <input
              id="reg-email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:border-primary-500 focus:outline-none transition-colors"
              required
            />
          </div>
          <div>
            <label htmlFor="reg-password" className="block text-sm text-gray-400 mb-1">Password</label>
            <input
              id="reg-password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:border-primary-500 focus:outline-none transition-colors"
              required
              minLength={8}
            />
            <p className="text-xs text-gray-500 mt-1">At least 8 characters</p>
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-primary-600 hover:bg-primary-700 disabled:opacity-50 text-white py-3 rounded-lg font-medium transition-colors"
          >
            {loading ? 'Creating account...' : 'Create Free Account'}
          </button>
        </form>
        <p className="text-center text-gray-400 mt-6 text-sm">
          Already have an account?{' '}
          <Link to="/login" className="text-primary-400 hover:text-primary-300">
            Log in
          </Link>
        </p>
      </div>
    </div>
  );
}
