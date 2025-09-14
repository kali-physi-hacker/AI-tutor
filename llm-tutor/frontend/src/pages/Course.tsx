import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'

type Course = { id: number; title: string; description?: string }
type Module = { id: number; title: string; index?: number }

export default function CoursePage() {
  const { id } = useParams()
  const [course, setCourse] = useState<Course | null>(null)
  const [modules, setModules] = useState<Module[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let active = true
    async function load() {
      try {
        setLoading(true)
        const [c, m] = await Promise.all([
          fetch(`/api/courses/${id}`).then(r => r.ok ? r.json() : Promise.reject(new Error('Course not found'))),
          fetch(`/api/courses/${id}/modules`).then(r => r.ok ? r.json() : [])
        ])
        if (!active) return
        setCourse(c)
        setModules(m)
      } catch (e: any) {
        setError(e.message || 'Failed to load course')
      } finally {
        setLoading(false)
      }
    }
    load()
    return () => { active = false }
  }, [id])

  if (loading) return <div className="max-w-4xl mx-auto p-6">Loading…</div>
  if (error) return <div className="max-w-4xl mx-auto p-6 text-red-600">{error}</div>
  if (!course) return <div className="max-w-4xl mx-auto p-6">Course not found.</div>

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">{course.title}</h1>
        <Link to="/courses" className="text-primary text-sm">Back to courses</Link>
      </div>
      {course.description && <p className="text-ink-soft">{course.description}</p>}
      <section>
        <h2 className="text-lg font-medium mb-2">Modules</h2>
        {modules.length === 0 && <div className="text-sm text-ink-soft">No modules yet.</div>}
        <ul className="grid gap-2">
          {modules.map(m => (
            <li key={m.id} className="card p-4">
              <div className="font-medium">{m.title}</div>
            </li>
          ))}
        </ul>
      </section>
    </div>
  )
}
