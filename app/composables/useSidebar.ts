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
      id: 'students',
      label: 'All Students',
      to: '/students',
      icon: 'i-lucide-user-check',
      description: 'Enrolled students directory and records'
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
      description: 'Center preferences and system settings',
      children: [
        {
          id: 'settings-staff',
          label: 'Staff',
          to: '/settings/staff',
          icon: 'i-lucide-user-cog',
          description: 'Staff accounts & role creation (Name, Role)'
        },
        {
          id: 'settings-courses',
          label: 'Courses',
          to: '/settings/courses',
          icon: 'i-lucide-book-open',
          description: 'Course catalog (Name, Level, Price)'
        },
        {
          id: 'settings-payments',
          label: 'Payment settings',
          to: '/settings/payments',
          icon: 'i-lucide-credit-card',
          description: 'Payment methods, Receiver, Quick pick notes'
        }
      ]
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
