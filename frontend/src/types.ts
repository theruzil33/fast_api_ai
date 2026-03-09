export interface Project {
  id: number
  name: string
  description: string | null
  created_at: string
}

export interface Filters {
  name: string
  sort_by: string
  order: string
}
