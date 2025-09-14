import { Link } from 'react-router-dom'

export default function Courses() {
  const sample = [
    { id: 1, title: 'Calculus I', description: 'Limits, derivatives, integrals' },
    { id: 2, title: 'Linear Algebra', description: 'Vectors and matrices' },
  ]
  return (
    <div className="max-w-5xl mx-auto p-6 grid gap-4">
      <h1 className="text-2xl">Courses</h1>
      <div className="grid md:grid-cols-2 gap-4">
        {sample.map(c => (
          <Link to={`/courses/${c.id}`} key={c.id} className="card p-6 hover:shadow-lift transition-shadow">
            <h3 className="text-lg font-medium">{c.title}</h3>
            <p className="text-ink-soft">{c.description}</p>
          </Link>
        ))}
      </div>
    </div>
  )
}
