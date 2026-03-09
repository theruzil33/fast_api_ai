import { useState } from 'react'
import { PageWrapper, Card, Title, Field, Label, Input, SubmitButton, ErrorText } from './index.styles'

interface LoginPageProps {
  onLogin: (token: string) => void
}

function LoginPage({ onLogin }: LoginPageProps) {
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    try {
      const res = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })

      const json = await res.json()

      if (!res.ok) {
        setError(json.error ?? `HTTP ${res.status}`)
        return
      }

      onLogin(json.access_token)
    } catch {
      setError('Network error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <PageWrapper>
      <Card>
        <Title>Sign in</Title>
        <form onSubmit={handleSubmit}>
          <Field>
            <Label>Username</Label>
            <Input
              required
              autoFocus
              value={form.username}
              onChange={(e) => setForm((prev) => ({ ...prev, username: e.target.value }))}
            />
          </Field>
          <Field>
            <Label>Password</Label>
            <Input
              required
              type="password"
              value={form.password}
              onChange={(e) => setForm((prev) => ({ ...prev, password: e.target.value }))}
            />
          </Field>
          {error && <ErrorText>{error}</ErrorText>}
          <SubmitButton type="submit" disabled={loading}>
            {loading ? 'Signing in…' : 'Sign in'}
          </SubmitButton>
        </form>
      </Card>
    </PageWrapper>
  )
}

export default LoginPage
