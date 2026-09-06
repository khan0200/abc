import { ref } from 'vue'
import type { Course } from '~/types/course'

const INITIAL_COURSES: Course[] = [
  {
    id: 'course-starter',
    name: 'Starter',
    level: 'Beginner',
    price: 180,
    currency: '$',
    description: 'Foundational English vocabulary & grammar',
    isActive: true
  },
  {
    id: 'course-elementary',
    name: 'Elementary',
    level: 'A1 - A2',
    price: 200,
    currency: '$',
    description: 'Basic conversational sentence structures',
    isActive: true
  },
  {
    id: 'course-intermediate',
    name: 'Intermediate',
    level: 'B1 - B2',
    price: 240,
    currency: '$',
    description: 'Fluent conversation and practical writing',
    isActive: true
  },
  {
    id: 'course-advanced',
    name: 'Advanced',
    level: 'C1',
    price: 280,
    currency: '$',
    description: 'Academic reading, debate, and advanced grammar',
    isActive: true
  },
  {
    id: 'course-ielts',
    name: 'IELTS Preparation',
    level: 'Exam Prep (6.5 - 8.0+)',
    price: 320,
    currency: '$',
    description: 'Intensive speaking, writing, and test strategies',
    isActive: true
  },
  {
    id: 'course-toefl',
    name: 'TOEFL iBT',
    level: 'Exam Prep',
    price: 320,
    currency: '$',
    description: 'Targeted preparation for university admissions',
    isActive: true
  },
  {
    id: 'course-korean',
    name: 'Korean Language',
    level: 'TOPIK I - II',
    price: 220,
    currency: '$',
    description: 'Hangul mastery, everyday conversation & culture',
    isActive: true
  },
  {
    id: 'course-chinese',
    name: 'Chinese (Mandarin)',
    level: 'HSK 1 - 4',
    price: 220,
    currency: '$',
    description: 'Pinyin, character writing, and practical dialog',
    isActive: true
  }
]

export const useCourses = () => {
  const courses = useState<Course[]>('crm-courses-catalog', () => INITIAL_COURSES)

  const addCourse = (data: Omit<Course, 'id'>) => {
    const newCourse: Course = {
      ...data,
      id: `course-${Date.now()}`,
      currency: data.currency || '$',
      isActive: data.isActive ?? true
    }
    courses.value.push(newCourse)
    return newCourse
  }

  const getCourseById = (id: string) => {
    return courses.value.find(c => c.id === id)
  }

  return {
    courses,
    addCourse,
    getCourseById
  }
}
