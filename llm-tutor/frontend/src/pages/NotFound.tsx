import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <div className="h-screen grid place-items-center p-6">
      <div className="text-center">
        <h1 className="text-3xl font-semibold">Page not found</h1>
        <p className="text-ink-soft mt-2">The page you’re looking for doesn’t exist.</p>
        <Link to="/" className="inline-block mt-4 bg-primary text-white px-4 py-2 rounded">Go home</Link>
      </div>
    </div>
  )
}

