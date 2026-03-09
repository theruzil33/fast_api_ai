import { useEffect, useState } from 'react'
import { Container, ErrorText, ActionsRow } from './index.styles'
import ProjectForm from './ProjectForm'
import ProjectsTable from './ProjectsTable'
import DeleteButton from './DeleteButton'
import ProjectsFilter from './ProjectsFilter'
import type { Project, Filters } from '../../types'

const DEFAULT_FILTERS: Filters = { name: '', sort_by: 'created_at', order: 'desc' }

interface ProjectsProps {
  token: string
  onUnauthorized: () => void
}

function Projects({ token, onUnauthorized }: ProjectsProps) {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selected, setSelected] = useState<Set<number>>(new Set())
  const [filters, setFilters] = useState<Filters>(DEFAULT_FILTERS)

  const authHeaders = { Authorization: `Bearer ${token}` }

  const handleApiError = async (res: Response): Promise<never> => {
    if (res.status === 401) {
      onUnauthorized()
    }
    const json = await res.json().catch(() => ({}))
    throw new Error(json.error ?? `HTTP ${res.status}`)
  }

  useEffect(() => {
    setLoading(true)
    const params = new URLSearchParams()
    if (filters.name) params.set('name', filters.name)
    params.set('sort_by', filters.sort_by)
    params.set('order', filters.order)

    fetch(`/api/v1/projects/?${params}`, { headers: authHeaders })
      .then(async (res) => {
        if (!res.ok) await handleApiError(res)
        return res.json()
      })
      .then((json: { data: Project[] }) => setProjects(json.data))
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false))
  }, [filters])

  const toggleSelect = (id: number) => {
    setSelected((prev) => {
      const next = new Set(prev)
      next.has(id) ? next.delete(id) : next.add(id)
      return next
    })
  }

  const handleDelete = async () => {
    try {
      await Promise.all(
        [...selected].map((id) =>
          fetch(`/api/v1/projects/${id}`, { method: 'DELETE', headers: authHeaders }).then(async (res) => {
            if (!res.ok) await handleApiError(res)
          })
        )
      )
      setProjects((prev) => prev.filter((p) => !selected.has(p.id)))
      setSelected(new Set())
    } catch (err) {
      setError((err as Error).message)
    }
  }

  return (
    <Container>
      <h1>Projects</h1>

      <ActionsRow>
        <ProjectForm token={token} onUnauthorized={onUnauthorized} onAdd={(project) => setProjects((prev) => [project, ...prev])} />
        <DeleteButton count={selected.size} onDelete={handleDelete} />
      </ActionsRow>

      <ProjectsFilter filters={filters} onChange={setFilters} />

      {loading && <p>Loading...</p>}
      {error && <ErrorText>Error: {error}</ErrorText>}

      {!loading && !error && (
        <ProjectsTable
          projects={projects}
          selected={selected}
          onToggle={toggleSelect}
        />
      )}
    </Container>
  )
}

export default Projects
