import { FilterRow, FilterField, Label, Input, Select } from './index.styles'
import type { Filters } from '../../types'

interface ProjectsFilterProps {
  filters: Filters
  onChange: (filters: Filters) => void
}

function ProjectsFilter({ filters, onChange }: ProjectsFilterProps) {
  return (
    <FilterRow>
      <FilterField>
        <Label>Name</Label>
        <Input
          placeholder="Search by name..."
          value={filters.name}
          onChange={(e) => onChange({ ...filters, name: e.target.value })}
        />
      </FilterField>
      <FilterField>
        <Label>Sort by</Label>
        <Select
          value={filters.sort_by}
          onChange={(e) => onChange({ ...filters, sort_by: e.target.value })}
        >
          <option value="created_at">Created At</option>
          <option value="name">Name</option>
        </Select>
      </FilterField>
      <FilterField>
        <Label>Order</Label>
        <Select
          value={filters.order}
          onChange={(e) => onChange({ ...filters, order: e.target.value })}
        >
          <option value="desc">Desc</option>
          <option value="asc">Asc</option>
        </Select>
      </FilterField>
    </FilterRow>
  )
}

export default ProjectsFilter
