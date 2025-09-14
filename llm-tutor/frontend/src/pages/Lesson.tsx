import { useParams } from 'react-router-dom'

export default function Lesson() {
  const { id } = useParams()
  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-2xl">Lesson {id}</h1>
      <article className="prose max-w-none mt-4">
        <p>Markdown content will render here.</p>
      </article>
    </div>
  )
}

