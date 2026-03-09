import { useState } from 'react'
import { Form, FormField, Label, Input, Textarea, SubmitButton, ErrorText } from './index.styles'
import type { Project } from '../../types'

interface ProjectFormProps {
  token: string
  onUnauthorized: () => void
  onAdd: (project: Project) => void
}

function ProjectForm({ token, onUnauthorized, onAdd }: ProjectFormProps) {
  const [form, setForm] = useState({ name: '', description: '' })
  const [formError, setFormError] = useState<string | null>(null)

  const handleSubmit = async (e: { preventDefault(): void }) => {
    e.preventDefault()
    setFormError(null)

    const res = await fetch('/api/v1/projects/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ name: form.name, description: form.description || null }),
    })

    if (!res.ok) {
      if (res.status === 401) onUnauthorized()
      const json = await res.json().catch(() => ({}))
      setFormError(json.error ?? `HTTP ${res.status}`)
      return
    }

    const json: { data: Project } = await res.json()
    onAdd(json.data)
    setForm({ name: '', description: '' })
  }

  return (
    <Form onSubmit={handleSubmit}>
      <FormField>
        <Label>Name</Label>
        <Input
          required
          value={form.name}
          onChange={(e) => setForm((prev) => ({ ...prev, name: e.target.value }))}
        />
      </FormField>
      <FormField>
        <Label>Description</Label>
        <Textarea
          value={form.description}
          onChange={(e) => setForm((prev) => ({ ...prev, description: e.target.value }))}
        />
      </FormField>
      {formError && <ErrorText>{formError}</ErrorText>}
      <SubmitButton type="submit">Add project</SubmitButton>
    </Form>
  )
}

export default ProjectForm
