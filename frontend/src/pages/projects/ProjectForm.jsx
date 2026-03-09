import { useState } from 'react'
import { Form, FormField, Label, Input, Textarea, SubmitButton, ErrorText } from './index.styles'

function ProjectForm({ onAdd }) {
  const [form, setForm] = useState({ name: '', description: '' })
  const [formError, setFormError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setFormError(null)

    const res = await fetch('/api/v1/projects/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: form.name, description: form.description || null }),
    })

    if (!res.ok) {
      const json = await res.json()
      setFormError(json.error ?? `HTTP ${res.status}`)
      return
    }

    const json = await res.json()
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
