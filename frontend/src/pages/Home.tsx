import { Link } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';

export default function Home() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);

  return (
    <div className="min-h-[calc(100vh-4rem)]">
      {/* Hero */}
      <section className="max-w-4xl mx-auto px-4 pt-20 pb-16 text-center">
        <div className="text-6xl mb-6">🐍</div>
        <h1 className="text-5xl font-bold mb-6">
          Learn Python <span className="text-primary-400">from Zero</span>
        </h1>
        <p className="text-xl text-gray-400 mb-8 max-w-2xl mx-auto">
          No coding experience needed. PyStarter teaches you Python step-by-step
          with interactive lessons, hands-on exercises, and AI-powered help when
          you're stuck.
        </p>
        <Link
          to={isAuthenticated ? '/dashboard' : '/register'}
          className="inline-block bg-primary-600 hover:bg-primary-700 text-white px-8 py-4 rounded-xl text-lg font-semibold transition-colors"
        >
          {isAuthenticated ? 'Continue Learning' : 'Start Learning — Free'}
        </Link>
      </section>

      {/* Features */}
      <section className="max-w-5xl mx-auto px-4 pb-20">
        <div className="grid md:grid-cols-3 gap-8">
          <FeatureCard
            emoji="📖"
            title="Learn, Then Practice"
            description="Each topic starts with a clear explanation, then interactive examples, then exercises. No guessing what to do."
          />
          <FeatureCard
            emoji="🧪"
            title="Instant Feedback"
            description="Write code and see results immediately. Friendly error messages tell you exactly what went wrong."
          />
          <FeatureCard
            emoji="🤖"
            title="AI Tutor"
            description="Stuck? Get hints from an AI tutor that explains things in simple, beginner-friendly language."
          />
          <FeatureCard
            emoji="🎯"
            title="Guided Path"
            description="Follow a structured curriculum from 'Hello World' to writing real programs. No overwhelm."
          />
          <FeatureCard
            emoji="🥋"
            title="Belt System"
            description="Earn XP and advance through belts as you learn. Track your progress and celebrate milestones."
          />
          <FeatureCard
            emoji="🐛"
            title="Beginner-Friendly"
            description="Exercises include fill-in-the-blank, fix-the-bug, and predict-the-output — not just 'write from scratch'."
          />
        </div>
      </section>

      {/* Curriculum Preview */}
      <section className="bg-gray-900/50 py-16">
        <div className="max-w-4xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-10">What You'll Learn</h2>
          <div className="space-y-3">
            {[
              { num: 1, title: 'Your First Program', desc: 'print(), comments, and running code' },
              { num: 2, title: 'Variables & Data Types', desc: 'Storing and using data' },
              { num: 3, title: 'Making Decisions', desc: 'if/elif/else statements' },
              { num: 4, title: 'Loops', desc: 'for loops and while loops' },
              { num: 5, title: 'Functions', desc: 'Reusable blocks of code' },
              { num: 6, title: 'Lists & Tuples', desc: 'Ordered collections' },
              { num: 7, title: 'Dictionaries', desc: 'Key-value data storage' },
              { num: 8, title: 'String Magic', desc: 'Text manipulation mastery' },
            ].map((m) => (
              <div
                key={m.num}
                className="flex items-center gap-4 bg-gray-800/50 rounded-lg px-5 py-4"
              >
                <span className="text-primary-400 font-bold text-lg w-8">{m.num}</span>
                <div>
                  <p className="font-semibold text-white">{m.title}</p>
                  <p className="text-sm text-gray-400">{m.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

function FeatureCard({ emoji, title, description }: { emoji: string; title: string; description: string }) {
  return (
    <div className="bg-gray-800/50 border border-gray-700/50 rounded-xl p-6">
      <div className="text-3xl mb-3">{emoji}</div>
      <h3 className="text-lg font-semibold mb-2 text-white">{title}</h3>
      <p className="text-gray-400 text-sm">{description}</p>
    </div>
  );
}
