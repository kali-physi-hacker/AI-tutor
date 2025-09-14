type Item = {
  document_id: number
  document_title: string
  chunk_index: number
  text: string
}

export default function CitationsPanel({ items }: { items: Item[] }) {
  if (!items?.length) {
    return <div className="text-sm text-ink-soft">No sources yet. Run a search.</div>
  }
  return (
    <div className="grid gap-3">
      {items.map((it, i) => (
        <div key={i} className="rounded-2xl border p-3 bg-paper-raised shadow-card">
          <div className="flex items-center justify-between">
            <div className="font-medium text-sm">{it.document_title} · #{it.chunk_index}</div>
          </div>
          <p className="text-sm text-ink-soft mt-2 whitespace-pre-wrap max-h-40 overflow-hidden">{it.text}</p>
        </div>
      ))}
    </div>
  )
}
