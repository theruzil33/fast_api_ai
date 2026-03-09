import { useEffect, useState } from 'react'
import { Container, ErrorText, ActionsRow } from './index.styles'
import ProjectForm from './ProjectForm'
import ProjectsTable from './ProjectsTable'
import DeleteButton from './DeleteButton'
import ProjectsFilter from './ProjectsFilter'
import type { Project, Filters } from '../../types'

const DEFAULT_FILTERS: Filters = { name: '', sort_by: 'created_at', order: 'desc' }

function Projects() {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selected, setSelected] = useState<Set<number>>(new Set())
  const [filters, setFilters] = useState<Filters>(DEFAULT_FILTERS)

  useEffect(() => {
    setLoading(true)
    const params = new URLSearchParams()
    if (filters.name) params.set('name', filters.name)
    params.set('sort_by', filters.sort_by)
    params.set('order', filters.order)

    fetch(`/api/v1/projects/?${params}`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
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
    await Promise.all(
      [...selected].map((id) =>
        fetch(`/api/v1/projects/${id}`, { method: 'DELETE' })
      )
    )
    setProjects((prev) => prev.filter((p) => !selected.has(p.id)))
    setSelected(new Set())
  }

  return (
    <Container>
      <h1>Projects</h1>

      <ActionsRow>
        <ProjectForm onAdd={(project) => setProjects((prev) => [project, ...prev])} />
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
