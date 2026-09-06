import { computed } from 'vue'
import type { Lead, LeadStatus, ClosedReason, CreateLeadInput } from '~/types/lead'
import { useCourses } from '~/composables/useCourses'

const SAMPLE_LEADS: Lead[] = [
  {
    id: 'lead-1',
    name: 'Min-jun Kim',
    phone: '010-3456-7890',
    courseId: 'course-ielts',
    courseName: 'IELTS Preparation',
    status: 'COLD',
    source: 'Instagram Ad',
    notes: 'Aiming for 7.0 band score for UK master study application.',
    preferredTime: 'Evening',
    assignedManager: 'David Miller',
    createdAt: new Date(Date.now() - 1000 * 60 * 45).toISOString(), // 45m ago
    updatedAt: new Date(Date.now() - 1000 * 60 * 45).toISOString()
  },
  {
    id: 'lead-2',
    name: 'Seo-yeon Lee',
    phone: '010-9123-4567',
    courseId: 'course-korean',
    courseName: 'Korean Language',
    status: 'COLD',
    source: 'Walk-in',
    notes: 'Inquired about weekend intermediate speaking class.',
    preferredTime: 'Weekend Morning',
    assignedManager: 'Sarah Jenkins',
    createdAt: new Date(Date.now() - 1000 * 60 * 180).toISOString(), // 3h ago
    updatedAt: new Date(Date.now() - 1000 * 60 * 180).toISOString()
  },
  {
    id: 'lead-3',
    name: 'Marcus Vance',
    phone: '+1 (415) 555-0199',
    courseId: 'course-intermediate',
    courseName: 'Intermediate',
    status: 'COLD',
    source: 'Website Form',
    notes: 'Expat working in Seoul looking to enhance conversation fluency.',
    preferredTime: 'Afternoon',
    assignedManager: 'David Miller',
    createdAt: new Date(Date.now() - 1000 * 60 * 360).toISOString(), // 6h ago
    updatedAt: new Date(Date.now() - 1000 * 60 * 360).toISOString()
  },
  {
    id: 'lead-4',
    name: 'Ji-woo Park',
    phone: '010-8765-4321',
    courseId: 'course-toefl',
    courseName: 'TOEFL iBT',
    status: 'WAITING',
    source: 'Referral',
    notes: 'Placement consultation complete. Waiting for schedule confirmation on Tuesday/Thursday.',
    preferredTime: 'Evening',
    assignedManager: 'David Miller',
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(), // 1 day ago
    updatedAt: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString()
  },
  {
    id: 'lead-5',
    name: 'Ha-eun Jung',
    phone: '010-2233-4455',
    courseId: 'course-starter',
    courseName: 'Starter',
    status: 'WAITING',
    source: 'KakaoTalk',
    notes: 'Ready to enroll. Invoice sent; preparing for next week orientation.',
    preferredTime: 'Morning',
    assignedManager: 'Sarah Jenkins',
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 36).toISOString(),
    updatedAt: new Date(Date.now() - 1000 * 60 * 60 * 4).toISOString()
  },
  {
    id: 'lead-6',
    name: 'Dong-hyun Choi',
    phone: '010-0000-0000',
    courseId: 'course-advanced',
    courseName: 'Advanced',
    status: 'CLOSED',
    closedReason: 'WRONG_NUMBER',
    source: 'Website Form',
    notes: 'Phone number was disconnected or answered by another party.',
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 72).toISOString(),
    updatedAt: new Date(Date.now() - 1000 * 60 * 60 * 12).toISOString()
  },
  {
    id: 'lead-7',
    name: 'Spam Marketing Inc.',
    phone: '+82 2-1234-5678',
    courseId: 'course-chinese',
    courseName: 'Chinese (Mandarin)',
    status: 'CLOSED',
    closedReason: 'IRRELEVANT',
    source: 'Website Form',
    notes: 'Commercial sales pitch submission instead of student inquiry.',
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 96).toISOString(),
    updatedAt: new Date(Date.now() - 1000 * 60 * 60 * 48).toISOString()
  }
]

export const useLeads = () => {
  const { getCourseById } = useCourses()
  const leads = useState<Lead[]>('crm-leads-data', () => SAMPLE_LEADS)

  // Filters
  const searchQuery = ref('')
  const selectedCourseId = ref<string>('all')

  const filteredLeads = computed(() => {
    const query = searchQuery.value.trim().toLowerCase()
    return leads.value.filter((lead) => {
      const matchesSearch = !query
        || lead.name.toLowerCase().includes(query)
        || lead.phone.replace(/[^0-9]/g, '').includes(query.replace(/[^0-9]/g, ''))
        || lead.courseName.toLowerCase().includes(query)

      const matchesCourse = selectedCourseId.value === 'all' || lead.courseId === selectedCourseId.value

      return matchesSearch && matchesCourse
    })
  })

  const coldLeads = computed(() => filteredLeads.value.filter(l => l.status === 'COLD'))
  const waitingLeads = computed(() => filteredLeads.value.filter(l => l.status === 'WAITING'))
  const closedLeads = computed(() => filteredLeads.value.filter(l => l.status === 'CLOSED'))

  const counts = computed(() => ({
    COLD: leads.value.filter(l => l.status === 'COLD').length,
    WAITING: leads.value.filter(l => l.status === 'WAITING').length,
    CLOSED: leads.value.filter(l => l.status === 'CLOSED').length,
    total: leads.value.length
  }))

  const addLead = (input: CreateLeadInput) => {
    const course = getCourseById(input.courseId)
    const newLead: Lead = {
      id: `lead-${Date.now()}`,
      name: input.name.trim(),
      phone: input.phone.trim(),
      courseId: input.courseId,
      courseName: course?.name || 'General Course',
      status: 'COLD', // New leads automatically placed in Cold
      notes: input.notes?.trim() || undefined,
      source: input.source || 'Direct Entry',
      preferredStartDate: input.preferredStartDate,
      preferredTime: input.preferredTime,
      assignedManager: input.assignedManager || 'Unassigned',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }

    leads.value.unshift(newLead)
    return newLead
  }

  const updateLeadStatus = (id: string, newStatus: LeadStatus, reason?: ClosedReason) => {
    const index = leads.value.findIndex(l => l.id === id)
    if (index !== -1) {
      const current = leads.value[index]
      if (current) {
        leads.value[index] = {
          ...current,
          status: newStatus,
          closedReason: newStatus === 'CLOSED' ? (reason || current.closedReason || 'NO_ANSWER') : undefined,
          updatedAt: new Date().toISOString()
        }
      }
    }
  }

  const reorderLead = (
    id: string,
    toStatus: LeadStatus,
    targetIndex: number,
    reason?: ClosedReason
  ) => {
    const leadIndex = leads.value.findIndex(l => l.id === id)
    if (leadIndex === -1) return

    const [lead] = leads.value.splice(leadIndex, 1)
    if (!lead) return

    lead.status = toStatus
    if (toStatus === 'CLOSED') {
      lead.closedReason = reason || lead.closedReason || 'NO_ANSWER'
    } else {
      lead.closedReason = undefined
    }
    lead.updatedAt = new Date().toISOString()

    // Find leads in the target status
    const statusLeads = leads.value.filter(l => l.status === toStatus)

    if (targetIndex >= statusLeads.length) {
      if (statusLeads.length > 0) {
        const last = statusLeads[statusLeads.length - 1]
        const lastIdx = leads.value.indexOf(last!)
        leads.value.splice(lastIdx + 1, 0, lead)
      } else {
        leads.value.push(lead)
      }
    } else {
      const targetLead = statusLeads[targetIndex]
      if (targetLead) {
        const insertIdx = leads.value.indexOf(targetLead)
        leads.value.splice(insertIdx, 0, lead)
      } else {
        leads.value.push(lead)
      }
    }
  }

  const deleteLead = (id: string) => {
    leads.value = leads.value.filter(l => l.id !== id)
  }

  return {
    leads,
    searchQuery,
    selectedCourseId,
    filteredLeads,
    coldLeads,
    waitingLeads,
    closedLeads,
    counts,
    addLead,
    updateLeadStatus,
    reorderLead,
    deleteLead
  }
}
