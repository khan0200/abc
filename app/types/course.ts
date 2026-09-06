export interface Course {
  id: string
  name: string
  level: string // e.g. 'Beginner', 'Intermediate', 'Advanced', 'Exam Prep', 'Language'
  price: number // e.g. 240
  currency?: string // e.g. '$' or '₩'
  description?: string
  isActive?: boolean
}
