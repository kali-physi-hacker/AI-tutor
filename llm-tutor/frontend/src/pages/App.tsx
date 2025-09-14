import { Link } from 'react-router-dom'

export default function App() {
  return (
    <div className="max-w-5xl mx-auto p-6">
      <header className="flex items-center justify-between py-6">
        <h1 className="text-2xl font-semibold">LLM Tutor</h1>
        <nav className="flex gap-4">
          <Link to="/courses" className="text-primary">Courses</Link>
          <Link to="/practice" className="text-primary">Practice</Link>
          <Link to="/login" className="text-primary">Login</Link>
        </nav>
      </header>
      <main className="grid gap-6 mt-10">
        <section className="card p-6">
          <h2 className="text-xl font-medium">Study with an AI Tutor</h2>
          <p className="text-ink-soft mt-2">Chat with a tutor that cites course sources and explains step-by-step.</p>
        </section>
      </main>
    </div>
  )
}

