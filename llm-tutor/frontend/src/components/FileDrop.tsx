import { useRef, useState } from 'react'
import { uploadDocument } from '../lib/api'

type Props = {
  onUploaded?: (res: any) => void
}

export default function FileDrop({ onUploaded }: Props) {
  const [dragging, setDragging] = useState(false)
  const [busy, setBusy] = useState(false)
  const [message, setMessage] = useState<string | null>(null)
  const [courseId, setCourseId] = useState<string>('')
  const [asyncIndex, setAsyncIndex] = useState(true)
  const inputRef = useRef<HTMLInputElement>(null)

  const onFiles = async (files: FileList | null) => {
    if (!files || !files[0]) return
    const f = files[0]
    setBusy(true); setMessage(null)
    try {
      const cid = courseId ? parseInt(courseId) : undefined
      const res = await uploadDocument(f, cid, asyncIndex)
      setMessage(`Uploaded: document_id=${res.document_id} chunks=${res.chunks}${res.scheduled ? ' (scheduled)' : ''}`)
      onUploaded?.(res)
    } catch (e: any) {
      setMessage(`Error: ${e.message || e}`)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="space-y-3">
      <div
        className={`border-2 border-dashed rounded-2xl p-6 text-center cursor-pointer ${dragging ? 'bg-paper-sunken' : ''}`}
        onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => { e.preventDefault(); setDragging(false); onFiles(e.dataTransfer.files) }}
        onClick={() => inputRef.current?.click()}
      >
        <p className="text-sm text-ink-soft">Drop a PDF/Markdown here or click to browse</p>
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.md,application/pdf,text/markdown,text/plain"
          className="hidden"
          onChange={(e) => onFiles(e.target.files)}
        />
      </div>
      <div className="flex items-center gap-3">
        <label className="text-sm">Course ID</label>
        <input value={courseId} onChange={e => setCourseId(e.target.value)} className="border rounded p-1 w-24" placeholder="optional" />
        <label className="text-sm flex items-center gap-2">
          <input type="checkbox" checked={asyncIndex} onChange={e => setAsyncIndex(e.target.checked)} />
          Async index
        </label>
        <button disabled={busy} className="ml-auto bg-primary text-white px-3 py-1 rounded" onClick={() => inputRef.current?.click()}>
          {busy ? 'Uploading...' : 'Choose file'}
        </button>
      </div>
      {message && <div className="text-sm text-ink-soft">{message}</div>}
    </div>
  )
}

