<script setup lang="ts">
import { ref } from 'vue'
import { useStudents } from '~/composables/useStudents'
import type { Student } from '~/types/student'
import StudentFilters from '~/components/students/StudentFilters.vue'
import StudentTable from '~/components/students/StudentTable.vue'
import EnrollStudentModal from '~/components/students/EnrollStudentModal.vue'
import StudentDetailModal from '~/components/students/StudentDetailModal.vue'

useSeoMeta({
  title: 'All Students • Education Center CRM',
  description: 'Complete roster of active, on-leave, and graduated students with filtering and course tracking.'
})

const { filteredStudents, stats, exportStudentsToCSV } = useStudents()

const isEnrollModalOpen = ref(false)
const selectedStudent = ref<Student | null>(null)
const isDetailModalOpen = ref(false)

const handleSelectStudent = (student: Student) => {
  selectedStudent.value = student
  isDetailModalOpen.value = true
}
</script>

<template>
  <div class="space-y-6">
    <!-- Top Header: Title, Subtitle, and Actions -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-4 border-b border-slate-200/80 dark:border-slate-800/80">
      <div>
        <div class="flex items-center gap-3">
          <h1 class="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">
            All Students
          </h1>
          <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-primary-50 text-primary-700 dark:bg-primary-950/60 dark:text-primary-300 border border-primary-200 dark:border-primary-900">
            {{ stats.total }} Enrolled
          </span>
        </div>
        <p class="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-0.5">
          Directory of enrolled students across all campuses, course programs, and academic cohorts.
        </p>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center gap-2.5">
        <button
          type="button"
          class="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 text-xs font-semibold shadow-2xs transition-colors cursor-pointer"
          title="Export student directory as CSV"
          @click="exportStudentsToCSV"
        >
          <UIcon
            name="i-lucide-download"
            class="w-4 h-4 text-slate-400"
          />
          <span>Export List</span>
        </button>

        <button
          type="button"
          class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-primary-600 hover:bg-primary-700 active:scale-[0.98] text-white text-xs font-bold shadow-sm shadow-primary-600/30 transition-all focus:outline-hidden cursor-pointer"
          @click="isEnrollModalOpen = true"
        >
          <UIcon
            name="i-lucide-user-plus"
            class="w-4 h-4"
          />
          <span>Enroll Student</span>
        </button>
      </div>
    </div>

    <!-- KPI Summary Metrics Grid -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- Card 1: Total -->
      <div class="p-4 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-2xs">
        <div class="flex items-center justify-between text-slate-500 mb-1">
          <span class="text-xs font-medium">Total Roster</span>
          <UIcon
            name="i-lucide-users"
            class="w-4 h-4 text-slate-400"
          />
        </div>
        <div class="flex items-baseline gap-2">
          <span class="text-2xl font-bold text-slate-900 dark:text-white">
            {{ stats.total }}
          </span>
          <span class="text-[11px] font-semibold text-emerald-600 dark:text-emerald-400">
            Active Center
          </span>
        </div>
      </div>

      <!-- Card 2: Active Students -->
      <div class="p-4 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-2xs">
        <div class="flex items-center justify-between text-slate-500 mb-1">
          <span class="text-xs font-medium">Active Learners</span>
          <UIcon
            name="i-lucide-graduation-cap"
            class="w-4 h-4 text-emerald-500"
          />
        </div>
        <div class="flex items-baseline gap-2">
          <span class="text-2xl font-bold text-emerald-600 dark:text-emerald-400">
            {{ stats.active }}
          </span>
          <span class="text-[11px] text-slate-400">
            Attending Classes
          </span>
        </div>
      </div>

      <!-- Card 3: On Leave -->
      <div class="p-4 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-2xs">
        <div class="flex items-center justify-between text-slate-500 mb-1">
          <span class="text-xs font-medium">On Leave</span>
          <UIcon
            name="i-lucide-clock"
            class="w-4 h-4 text-amber-500"
          />
        </div>
        <div class="flex items-baseline gap-2">
          <span class="text-2xl font-bold text-amber-600 dark:text-amber-400">
            {{ stats.onLeave }}
          </span>
          <span class="text-[11px] text-slate-400">
            Temporary Hold
          </span>
        </div>
      </div>

      <!-- Card 4: Outstanding Tuition -->
      <div class="p-4 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-2xs">
        <div class="flex items-center justify-between text-slate-500 mb-1">
          <span class="text-xs font-medium">Pending Tuition</span>
          <UIcon
            name="i-lucide-wallet"
            class="w-4 h-4 text-rose-500"
          />
        </div>
        <div class="flex items-baseline gap-2">
          <span class="text-2xl font-bold text-slate-900 dark:text-white">
            ${{ stats.totalOverdue }}
          </span>
          <span class="text-[11px] font-semibold text-rose-600 dark:text-rose-400">
            Unsettled
          </span>
        </div>
      </div>
    </div>

    <!-- Search & Filter Controls -->
    <StudentFilters />

    <!-- Table Roster View -->
    <StudentTable
      :students="filteredStudents"
      @select="handleSelectStudent"
    />

    <!-- Enroll Student Modal -->
    <EnrollStudentModal
      v-model="isEnrollModalOpen"
    />

    <!-- Student Detail Modal -->
    <StudentDetailModal
      :student="selectedStudent"
      :is-open="isDetailModalOpen"
      @close="isDetailModalOpen = false"
    />
  </div>
</template>
