import { useState } from 'react'
import FileDrop from '../components/FileDrop'
import { ragReindex } from '../lib/api'

export default function Admin() {
  const [reindexMsg, setReindexMsg] = useState<string | null>(null)

  const handleReindex = async () => {
    setReindexMsg('Scheduling reindex...')
    try {
      const res = await ragReindex()
      setReindexMsg(`Reindex scheduled (${res.count ?? 0} docs)`) 
    } catch (e: any) {
      setReindexMsg(`Error: ${e.message || e}`)
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl">Admin</h1>
      <div className="grid md:grid-cols-2 gap-4 mt-4">
        <div className="card p-4">
          <h2 className="font-medium mb-3">Upload Documents</h2>
          <FileDrop />
        </div>
        <div className="card p-4 space-y-3">
          <h2 className="font-medium">Reindex Corpus</h2>
          <button className="bg-primary text-white px-3 py-2 rounded" onClick={handleReindex}>Reindex</button>
          {reindexMsg && <div className="text-sm text-ink-soft">{reindexMsg}</div>}
          <div className="mt-4">Analytics</div>
        </div>
      </div>
    </div>
  )
}
