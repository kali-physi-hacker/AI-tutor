import { useEffect, useRef, useState } from 'react'
import { useParams } from 'react-router-dom'
import CitationsPanel from '../components/CitationsPanel'
import { ragSearch } from '../lib/api'

export default function Chat() {
  const { chatId } = useParams()
  const [lines, setLines] = useState<string[]>([])
  const [input, setInput] = useState('')
  const sseRef = useRef<EventSource | null>(null)
  const [query, setQuery] = useState('')
  const [sources, setSources] = useState<any[]>([])
  const [searching, setSearching] = useState(false)

  useEffect(() => {
    if (!chatId) return
    const sse = new EventSource(`/api/chats/${chatId}/stream`)
    sse.onmessage = (e) => setLines(l => [...l, e.data])
    sse.onerror = () => sse.close()
    sseRef.current = sse
    return () => sse.close()
  }, [chatId])

  return (
    <div className="grid grid-cols-12 gap-4 h-screen p-4">
      <aside className="col-span-3 card p-4">History</aside>
      <main className="col-span-6 card p-4 flex flex-col">
        <div className="flex-1 overflow-auto space-y-2">
          {lines.map((l, i) => (
            <div key={i} className="text-sm text-ink-soft">{l}</div>
          ))}
        </div>
        <form
          className="mt-4 flex gap-2"
          onSubmit={e => { e.preventDefault(); setInput('') }}
        >
          <input className="border rounded p-2 flex-1" value={input} onChange={e => setInput(e.target.value)} placeholder="Ask about the lesson..." />
          <button className="bg-primary text-white px-3 rounded">Send</button>
        </form>
      </main>
      <aside className="col-span-3 card p-4 flex flex-col">
        <h2 className="font-medium mb-2">Sources</h2>
        <form
          className="flex gap-2 mb-3"
          onSubmit={async (e) => { e.preventDefault(); setSearching(true); try { const res = await ragSearch(query || input, 6); setSources(res.chunks || []) } finally { setSearching(false) } }}
        >
          <input className="border rounded p-2 flex-1" value={query} onChange={e => setQuery(e.target.value)} placeholder="Search context..." />
          <button className="bg-primary text-white px-3 rounded">{searching ? '...' : 'Search'}</button>
        </form>
        <div className="flex-1 overflow-auto"><CitationsPanel items={sources} /></div>
        <div className="mt-3">Tools</div>
      </aside>
    </div>
  )
}
