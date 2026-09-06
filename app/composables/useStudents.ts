import { ref, computed } from 'vue'
import type { Student, StudentStatus } from '~/types/student'
import { useCourses } from '~/composables/useCourses'

const SAMPLE_STUDENTS: Student[] = [
  {
    id: 'student-1',
    studentId: 'STU-2026-001',
    name: 'Min-jun Kim',
    email: 'minjun.kim@student.edu',
    phone: '010-3456-7890',
    guardianName: 'Hyun-woo Kim',
    guardianPhone: '010-1122-3344',
    courseId: 'course-ielts',
    courseName: 'IELTS Preparation',
    groupName: 'IELTS Morning A (Mon/Wed/Fri)',
    branch: 'Central Campus',
    status: 'ACTIVE',
    tuitionStatus: 'PAID',
    balance: 0,
    attendanceRate: 98,
    enrolledAt: '2026-08-15',
    notes: 'Aiming for 7.5 band score. Top performer in mock tests.'
  },
  {
    id: 'student-2',
    studentId: 'STU-2026-002',
    name: 'Ji-woo Park',
    email: 'jiwoo.park@student.edu',
    phone: '010-8765-4321',
    guardianName: 'Eun-sook Choi',
    guardianPhone: '010-5566-7788',
    courseId: 'course-toefl',
    courseName: 'TOEFL iBT',
    groupName: 'TOEFL Evening B (Tue/Thu)',
    branch: 'Downtown Branch',
    status: 'ACTIVE',
    tuitionStatus: 'PENDING',
    balance: 160,
    attendanceRate: 92,
    enrolledAt: '2026-08-20',
    notes: 'Invoice sent for remaining term installment.'
  },
  {
    id: 'student-3',
    studentId: 'STU-2026-003',
    name: 'Seo-yeon Lee',
    email: 'seoyeon.lee@student.edu',
    phone: '010-9123-4567',
    courseId: 'course-korean',
    courseName: 'Korean Language',
    groupName: 'TOPIK II Weekend Intensive',
    branch: 'Central Campus',
    status: 'ACTIVE',
    tuitionStatus: 'PAID',
    balance: 0,
    attendanceRate: 100,
    enrolledAt: '2026-07-10',
    notes: 'Preparing for TOPIK Level 4 examination.'
  },
  {
    id: 'student-4',
    studentId: 'STU-2026-004',
    name: 'Alex Johnson',
    email: 'alex.johnson@student.edu',
    phone: '+1 (555) 019-6102',
    guardianName: 'Robert Johnson',
    guardianPhone: '+1 (555) 019-9401',
    courseId: 'course-starter',
    courseName: 'Starter',
    groupName: 'Starter A1 Morning (Mon-Fri)',
    branch: 'Central Campus',
    status: 'ON_LEAVE',
    tuitionStatus: 'PAID',
    balance: 0,
    attendanceRate: 88,
    enrolledAt: '2026-06-01',
    notes: 'Medical leave until end of September.'
  },
  {
    id: 'student-5',
    studentId: 'STU-2026-005',
    name: 'Ha-eun Jung',
    email: 'haeun.jung@student.edu',
    phone: '010-2233-4455',
    guardianName: 'Sang-hoon Jung',
    guardianPhone: '010-9988-7766',
    courseId: 'course-intermediate',
    courseName: 'Intermediate',
    groupName: 'Conversation Club (Tue/Thu)',
    branch: 'Downtown Branch',
    status: 'ACTIVE',
    tuitionStatus: 'OVERDUE',
    balance: 240,
    attendanceRate: 85,
    enrolledAt: '2026-08-01',
    notes: 'Payment reminder sent to guardian via KakaoTalk.'
  },
  {
    id: 'student-6',
    studentId: 'STU-2026-006',
    name: 'Marcus Vance',
    email: 'marcus.vance@student.edu',
    phone: '+1 (415) 555-0199',
    courseId: 'course-korean',
    courseName: 'Korean Language',
    groupName: 'Expat Practical Korean (Evening)',
    branch: 'Central Campus',
    status: 'ACTIVE',
    tuitionStatus: 'PAID',
    balance: 0,
    attendanceRate: 95,
    enrolledAt: '2026-08-25',
    notes: 'Company sponsored enrollment.'
  },
  {
    id: 'student-7',
    studentId: 'STU-2026-007',
    name: 'Dong-hyun Choi',
    email: 'donghyun.choi@student.edu',
    phone: '010-4455-6677',
    courseId: 'course-advanced',
    courseName: 'Advanced',
    groupName: 'C1 Academic Writing & Debate',
    branch: 'Central Campus',
    status: 'GRADUATED',
    tuitionStatus: 'PAID',
    balance: 0,
    attendanceRate: 99,
    enrolledAt: '2026-01-15',
    notes: 'Completed C1 diploma. Transitioned to alumni network.'
  },
  {
    id: 'student-8',
    studentId: 'STU-2026-008',
    name: 'Chloe Dubois',
    email: 'chloe.dubois@student.edu',
    phone: '+33 6 12 34 56 78',
    courseId: 'course-chinese',
    courseName: 'Chinese (Mandarin)',
    groupName: 'HSK 3 Fast-Track',
    branch: 'Downtown Branch',
    status: 'ACTIVE',
    tuitionStatus: 'PAID',
    balance: 0,
    attendanceRate: 94,
    enrolledAt: '2026-08-12',
    notes: 'Fast learner, transferred from Shanghai branch.'
  },
  {
    id: 'student-9',
    studentId: 'STU-2026-009',
    name: 'Ye-jun Kang',
    email: 'yejun.kang@student.edu',
    phone: '010-3344-5566',
    guardianName: 'Myung-hee Kang',
    courseId: 'course-ielts',
    courseName: 'IELTS Preparation',
    groupName: 'IELTS Weekend Prep',
    branch: 'Central Campus',
    status: 'INACTIVE',
    tuitionStatus: 'OVERDUE',
    balance: 320,
    attendanceRate: 64,
    enrolledAt: '2026-05-10',
    notes: 'Suspended enrollment due to consecutive absences.'
  },
  {
    id: 'student-10',
    studentId: 'STU-2026-010',
    name: 'Soo-ah Shin',
    email: 'sooah.shin@student.edu',
    phone: '010-7788-9900',
    guardianName: 'Jin-woo Shin',
    guardianPhone: '010-3322-1100',
    courseId: 'course-starter',
    courseName: 'Starter',
    groupName: 'Evening Foundations A',
    branch: 'Downtown Branch',
    status: 'ACTIVE',
    tuitionStatus: 'PAID',
    balance: 0,
    attendanceRate: 96,
    enrolledAt: '2026-09-01',
    notes: 'Enrolled via August referral campaign.'
  }
]

export const useStudents = () => {
  const students = useState<Student[]>('crm-students-data', () => SAMPLE_STUDENTS)

  // Filter States
  const searchQuery = ref('')
  const selectedCourse = ref('all')
  const selectedStatus = ref('all')
  const selectedBranch = ref('all')

  const filteredStudents = computed(() => {
    const query = searchQuery.value.trim().toLowerCase()
    const cleanNumbers = query.replace(/[^0-9]/g, '')

    return students.value.filter(s => {
      // Search matches: name, studentId, email, phone, guardian
      const matchesSearch = !query ||
        s.name.toLowerCase().includes(query) ||
        s.studentId.toLowerCase().includes(query) ||
        s.email.toLowerCase().includes(query) ||
        (cleanNumbers && s.phone.replace(/[^0-9]/g, '').includes(cleanNumbers)) ||
        (s.guardianName && s.guardianName.toLowerCase().includes(query))

      // Course Filter
      const matchesCourse = selectedCourse.value === 'all' || s.courseId === selectedCourse.value

      // Status Filter
      const matchesStatus = selectedStatus.value === 'all' || s.status === selectedStatus.value

      // Branch Filter
      const matchesBranch = selectedBranch.value === 'all' || s.branch === selectedBranch.value

      return matchesSearch && matchesCourse && matchesStatus && matchesBranch
    })
  })

  // Summary KPI Metrics
  const stats = computed(() => {
    const total = students.value.length
    const active = students.value.filter(s => s.status === 'ACTIVE').length
    const onLeave = students.value.filter(s => s.status === 'ON_LEAVE').length
    const graduated = students.value.filter(s => s.status === 'GRADUATED').length
    const totalOverdue = students.value.reduce((sum, s) => sum + s.balance, 0)

    return {
      total,
      active,
      onLeave,
      graduated,
      totalOverdue
    }
  })

  const resetFilters = () => {
    searchQuery.value = ''
    selectedCourse.value = 'all'
    selectedStatus.value = 'all'
    selectedBranch.value = 'all'
  }

  const updateStudentStatus = (id: string, newStatus: StudentStatus) => {
    const s = students.value.find(item => item.id === id)
    if (s) {
      s.status = newStatus
    }
  }

  const enrollStudent = (data: {
    name: string
    email: string
    phone: string
    courseId: string
    groupName: string
    branch?: string
    guardianName?: string
    guardianPhone?: string
    notes?: string
  }) => {
    const { getCourseById } = useCourses()
    const course = getCourseById(data.courseId)
    const newStudent: Student = {
      id: `student-${Date.now()}`,
      studentId: `STU-2026-${String(students.value.length + 1).padStart(3, '0')}`,
      name: data.name.trim(),
      email: data.email.trim(),
      phone: data.phone.trim(),
      guardianName: data.guardianName?.trim() || undefined,
      guardianPhone: data.guardianPhone?.trim() || undefined,
      courseId: data.courseId,
      courseName: course?.name || 'General Course',
      groupName: data.groupName.trim() || 'General Cohort',
      branch: data.branch || 'Central Campus',
      status: 'ACTIVE',
      tuitionStatus: 'PAID',
      balance: 0,
      attendanceRate: 100,
      enrolledAt: new Date().toISOString().slice(0, 10),
      notes: data.notes?.trim() || undefined
    }

    students.value.unshift(newStudent)
    return newStudent
  }

  const exportStudentsToCSV = () => {
    if (typeof window === 'undefined' || filteredStudents.value.length === 0) return

    const headers = ['Student ID', 'Full Name', 'Email', 'Phone', 'Course', 'Group', 'Branch', 'Status', 'Attendance', 'Balance', 'Enrolled Date']
    const rows = filteredStudents.value.map(s => [
      `"${s.studentId}"`,
      `"${s.name.replace(/"/g, '""')}"`,
      `"${s.email.replace(/"/g, '""')}"`,
      `"${s.phone}"`,
      `"${s.courseName.replace(/"/g, '""')}"`,
      `"${s.groupName.replace(/"/g, '""')}"`,
      `"${s.branch}"`,
      `"${s.status}"`,
      `"${s.attendanceRate ?? 100}%"`,
      `"${s.balance}"`,
      `"${s.enrolledAt}"`
    ])

    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n')
    const encodedUri = encodeURI(csvContent)
    const link = document.createElement('a')
    link.setAttribute('href', encodedUri)
    link.setAttribute('download', `students_roster_${new Date().toISOString().slice(0, 10)}.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return {
    students,
    searchQuery,
    selectedCourse,
    selectedStatus,
    selectedBranch,
    filteredStudents,
    stats,
    resetFilters,
    updateStudentStatus,
    enrollStudent,
    exportStudentsToCSV
  }
}

