import { Table, Thead, Th, Tr, Td, EmptyTd } from './index.styles'

function ProjectsTable({ projects, selected, onToggle }) {
  return (
    <Table>
      <Thead>
        <tr>
          <Th />
          <Th>ID</Th>
          <Th>Name</Th>
          <Th>Description</Th>
          <Th>Created At</Th>
        </tr>
      </Thead>
      <tbody>
        {projects.length === 0 ? (
          <tr>
            <EmptyTd colSpan={5}>No projects found</EmptyTd>
          </tr>
        ) : (
          projects.map((p) => (
            <Tr key={p.id}>
              <Td>
                <input
                  type="checkbox"
                  checked={selected.has(p.id)}
                  onChange={() => onToggle(p.id)}
                />
              </Td>
              <Td>{p.id}</Td>
              <Td>{p.name}</Td>
              <Td>{p.description ?? '—'}</Td>
              <Td>{new Date(p.created_at).toLocaleString()}</Td>
            </Tr>
          ))
        )}
      </tbody>
    </Table>
  )
}

export default ProjectsTable
