import { getAuthToken } from '../store/auth'

const base = '' // proxied via Vite to backend

async function apiFetch(path: string, init: RequestInit = {}) {
  const token = getAuthToken()
  const headers = new Headers(init.headers || {})
  headers.set('Accept', 'application/json')
  if (!(init.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json')
  }
  if (token) headers.set('Authorization', `Bearer ${token}`)
  const res = await fetch(base + path, { credentials: 'include', ...init, headers })
  if (!res.ok) {
    const msg = await res.text().catch(() => res.statusText)
    throw new Error(msg || `HTTP ${res.status}`)
  }
  const ct = res.headers.get('content-type') || ''
  return ct.includes('application/json') ? res.json() : res.text()
}

export async function login(email: string, password: string) {
  return apiFetch('/api/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) })
}

export async function register(email: string, password: string) {
  return apiFetch('/api/auth/register', { method: 'POST', body: JSON.stringify({ email, password }) })
}

export async function uploadDocument(file: File, courseId?: number, asyncIndex = true) {
  const fd = new FormData()
  fd.append('file', file)
  if (courseId != null) fd.append('course_id', String(courseId))
  fd.append('async_index', String(asyncIndex))
  const token = getAuthToken()
  const headers = new Headers()
  if (token) headers.set('Authorization', `Bearer ${token}`)
  const res = await fetch('/api/documents/upload', {
    method: 'POST',
    body: fd,
    headers,
    credentials: 'include'
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function ragSearch(query: string, k = 6) {
  return apiFetch('/api/rag/search', { method: 'POST', body: JSON.stringify({ query, k }) })
}

export async function ragReindex() {
  return apiFetch('/api/rag/reindex', { method: 'POST' })
}

