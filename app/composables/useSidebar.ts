import type { NavItem } from '~/types/navigation'

export const useSidebar = () => {
  const isMobileOpen = useState<boolean>('sidebar-mobile-open', () => false)
  const isCollapsed = useState<boolean>('sidebar-desktop-collapsed', () => false)

  const navItems: NavItem[] = [
    {
      id: 'home',
      label: 'Home',
      to: '/',
      icon: 'i-lucide-home',
      description: 'Center overview and key metrics'
    },
    {
      id: 'leads',
      label: 'Leads',
      to: '/leads',
      icon: 'i-lucide-user-plus',
      description: 'Prospective students and inquiries'
    },
    {
      id: 'staff',
      label: 'Staff',
      to: '/staff',
      icon: 'i-lucide-graduation-cap',
      description: 'Instructors, mentors and administrators'
    },
    {
      id: 'rooms',
      label: 'Rooms',
      to: '/rooms',
      icon: 'i-lucide-door-open',
      description: 'Classrooms, labs and availability'
    },
    {
      id: 'groups',
      label: 'Groups',
      to: '/groups',
      icon: 'i-lucide-users',
      description: 'Student cohorts, classes and study groups'
    },
    {
      id: 'finance',
      label: 'Finance',
      to: '/finance',
      icon: 'i-lucide-wallet',
      description: 'Tuition, invoices and accounts'
    },
    {
      id: 'settings',
      label: 'Settings',
      to: '/settings',
      icon: 'i-lucide-settings',
      description: 'Center preferences and system settings'
    }
  ]

  const toggleMobile = () => {
    isMobileOpen.value = !isMobileOpen.value
  }

  const closeMobile = () => {
    isMobileOpen.value = false
  }

  const openMobile = () => {
    isMobileOpen.value = true
  }

  const toggleCollapse = () => {
    isCollapsed.value = !isCollapsed.value
  }

  return {
    isMobileOpen,
    isCollapsed,
    navItems,
    toggleMobile,
    closeMobile,
    openMobile,
    toggleCollapse
  }
}
