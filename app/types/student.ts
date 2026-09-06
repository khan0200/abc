export type StudentStatus = 'ACTIVE' | 'ON_LEAVE' | 'GRADUATED' | 'INACTIVE'

export type TuitionStatus = 'PAID' | 'PENDING' | 'OVERDUE'

export interface Student {
  id: string
  studentId: string // e.g. "STU-2026-001"
  name: string
  email: string
  phone: string
  guardianName?: string
  guardianPhone?: string
  courseId: string
  courseName: string
  groupName: string // e.g. "Group A (Mon/Wed)"
  branch: string // e.g. "Central Campus" | "Downtown Branch"
  status: StudentStatus
  tuitionStatus: TuitionStatus
  balance: number // Current due amount (0 if paid)
  attendanceRate?: number // e.g. 96 (%)
  enrolledAt: string
  notes?: string
}

export interface StudentFilterOptions {
  search: string
  courseId: string
  status: string
  branch: string
}
