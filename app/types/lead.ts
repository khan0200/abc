export type LeadStatus = 'COLD' | 'WAITING' | 'CLOSED'

export type ClosedReason = 'NO_ANSWER' | 'WRONG_NUMBER' | 'IRRELEVANT' | 'OTHER'

export interface Lead {
  id: string
  name: string
  phone: string
  courseId: string
  courseName: string
  status: LeadStatus
  closedReason?: ClosedReason
  notes?: string
  source?: string
  preferredStartDate?: string
  preferredTime?: string
  assignedManager?: string
  createdAt: string
  updatedAt: string
}

export interface CreateLeadInput {
  name: string
  phone: string
  courseId: string
  notes?: string
  source?: string
  preferredStartDate?: string
  preferredTime?: string
  assignedManager?: string
}
