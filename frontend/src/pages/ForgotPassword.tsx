import { useState } from 'react';
import { Link } from 'react-router-dom';
import { requestPasswordReset } from '../api/auth';

export default function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await requestPasswordReset(email);
    } catch {
      // Show success regardless (anti-enumeration)
    } finally {
      setSubmitted(true);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <h1 className="text-3xl font-bold text-center mb-2">Reset Password</h1>
        <p className="text-gray-400 text-center mb-8">
          Enter your email and we'll send you a reset link.
        </p>

        {submitted ? (
          <div className="bg-green-500/10 border border-green-500/30 text-green-400 px-4 py-4 rounded-lg text-sm text-center">
            If an account with that email exists, a reset link has been sent. Check your inbox.
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="reset-email" className="block text-sm text-gray-400 mb-1">
                Email
              </label>
              <input
                id="reset-email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:border-primary-500 focus:outline-none transition-colors"
                required
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-primary-600 hover:bg-primary-700 disabled:opacity-50 text-white py-3 rounded-lg font-medium transition-colors"
            >
              {loading ? 'Sending...' : 'Send Reset Link'}
            </button>
          </form>
        )}

        <p className="text-center text-gray-400 mt-6 text-sm">
          <Link to="/login" className="text-primary-400 hover:text-primary-300">
            Back to Login
          </Link>
        </p>
      </div>
    </div>
  );
}
