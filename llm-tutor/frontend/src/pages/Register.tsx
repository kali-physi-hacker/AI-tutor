import { useState } from 'react'
import { register } from '../lib/api'
import { useAuth } from '../store/auth'

export default function Register() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [msg, setMsg] = useState<string | null>(null)
  const setToken = useAuth(s => s.setToken)
  return (
    <div className="max-w-md mx-auto p-6">
      <h1 className="text-2xl mb-4">Register</h1>
      <form className="grid gap-4 card p-6" onSubmit={async (e) => {
        e.preventDefault()
        setMsg('Creating account...')
        try {
          const res = await register(email, password)
          setToken(res.access_token)
          setMsg('Account created')
        } catch (e: any) {
          setMsg(`Error: ${e.message || e}`)
        }
      }}>
        <input className="border rounded p-2" placeholder="Email" type="email" value={email} onChange={e => setEmail(e.target.value)} />
        <input className="border rounded p-2" placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
        <button className="bg-primary text-white px-4 py-2 rounded">Create account</button>
        {msg && <div className="text-sm text-ink-soft">{msg}</div>}
      </form>
    </div>
  )
}
