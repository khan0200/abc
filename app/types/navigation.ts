export interface NavItem {
  id: string
  label: string
  to: string
  icon: string
  badge?: string | number
  badgeColor?: 'neutral' | 'primary' | 'success' | 'warning' | 'error' | 'info'
  exact?: boolean
  description?: string
  children?: NavItem[]
}

export interface NavSection {
  title?: string
  items: NavItem[]
}
