<script setup lang="ts">
import { ref } from 'vue'
import type { Student } from '~/types/student'

const props = defineProps<{
  students: Student[]
}>()

const emit = defineEmits<{
  (e: 'select', student: Student): void
}>()

const copiedId = ref<string | null>(null)

const copyText = async (id: string, text: string) => {
  try {
    await navigator.clipboard.writeText(text)
    copiedId.value = id
    setTimeout(() => {
      copiedId.value = null
    }, 1500)
  } catch (err) {
    console.error('Copy failed', err)
  }
}
</script>

<template>
  <div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-2xs overflow-hidden">
    <!-- Responsive Table Container with Horizontal Scroll on Mobile -->
    <div class="overflow-x-auto">
      <table class="w-full text-left border-collapse">
        <!-- Table Header -->
        <thead>
          <tr class="border-b border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-slate-950/60 text-[11px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
            <th class="py-3.5 px-4 sm:px-6">Student</th>
            <th class="py-3.5 px-4">Contact Info</th>
            <th class="py-3.5 px-4">Course & Group</th>
            <th class="py-3.5 px-4">Campus</th>
            <th class="py-3.5 px-4 text-center">Status</th>
            <th class="py-3.5 px-4 text-center">Attendance</th>
            <th class="py-3.5 px-4 text-right">Tuition Balance</th>
            <th class="py-3.5 px-4 text-center">Action</th>
          </tr>
        </thead>

        <!-- Table Body -->
        <tbody class="divide-y divide-slate-100 dark:divide-slate-800/70 text-xs">
          <tr
            v-for="student in students"
            :key="student.id"
            class="hover:bg-slate-50/80 dark:hover:bg-slate-800/40 transition-colors group cursor-pointer"
            @click="emit('select', student)"
          >
            <!-- Column 1: Student Identity -->
            <td class="py-3.5 px-4 sm:px-6">
              <div class="flex items-center gap-3">
                <!-- Avatar Initials -->
                <div class="w-9 h-9 rounded-xl bg-primary-50 text-primary-700 dark:bg-primary-950/80 dark:text-primary-300 font-bold text-xs flex items-center justify-center ring-1 ring-primary-500/20 shrink-0">
                  {{ student.name.charAt(0).toUpperCase() }}
                </div>

                <div class="min-w-0">
                  <div class="flex items-center gap-1.5">
                    <span class="font-bold text-slate-900 dark:text-white truncate">
                      {{ student.name }}
                    </span>
                    <span class="px-1.5 py-0.2 rounded text-[10px] font-mono font-semibold bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400">
                      {{ student.studentId }}
                    </span>
                  </div>
                  <span class="text-[11px] text-slate-400 truncate block">
                    {{ student.email }}
                  </span>
                </div>
              </div>
            </td>

            <!-- Column 2: Contact Info -->
            <td class="py-3.5 px-4">
              <div class="flex flex-col">
                <div class="flex items-center gap-1.5">
                  <span class="font-mono text-slate-800 dark:text-slate-200 font-medium">
                    {{ student.phone }}
                  </span>
                  <button
                    type="button"
                    class="p-0.5 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
                    :title="copiedId === student.id ? 'Copied!' : 'Copy phone'"
                    @click.stop="copyText(student.id, student.phone)"
                  >
                    <UIcon :name="copiedId === student.id ? 'i-lucide-check' : 'i-lucide-copy'" class="w-3 h-3 text-primary-600" />
                  </button>
                </div>
                <span v-if="student.guardianName" class="text-[10px] text-slate-400 truncate">
                  Guardian: {{ student.guardianName }}
                </span>
              </div>
            </td>

            <!-- Column 3: Course & Cohort Group -->
            <td class="py-3.5 px-4">
              <div class="flex flex-col gap-0.5">
                <span class="font-semibold text-slate-900 dark:text-white truncate max-w-[200px]">
                  {{ student.courseName }}
                </span>
                <span class="text-[11px] text-slate-500 dark:text-slate-400 truncate max-w-[220px]">
                  {{ student.groupName }}
                </span>
              </div>
            </td>

            <!-- Column 4: Campus Branch -->
            <td class="py-3.5 px-4">
              <span class="inline-flex items-center gap-1 text-slate-700 dark:text-slate-300">
                <UIcon name="i-lucide-building" class="w-3.5 h-3.5 text-slate-400" />
                <span>{{ student.branch }}</span>
              </span>
            </td>

            <!-- Column 5: Status Badge -->
            <td class="py-3.5 px-4 text-center">
              <span
                :class="[
                  'inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-semibold border',
                  student.status === 'ACTIVE'
                    ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800'
                    : student.status === 'ON_LEAVE'
                      ? 'bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300 border-amber-200 dark:border-amber-800'
                      : student.status === 'GRADUATED'
                        ? 'bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-300 border-blue-200 dark:border-blue-800'
                        : 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border-slate-200 dark:border-slate-700'
                ]"
              >
                <span
                  :class="[
                    'w-1.5 h-1.5 rounded-full',
                    student.status === 'ACTIVE'
                      ? 'bg-emerald-500'
                      : student.status === 'ON_LEAVE'
                        ? 'bg-amber-500'
                        : student.status === 'GRADUATED'
                          ? 'bg-blue-500'
                          : 'bg-slate-400'
                  ]"
                />
                <span>{{ student.status.replace('_', ' ') }}</span>
              </span>
            </td>

            <!-- Column 6: Attendance -->
            <td class="py-3.5 px-4 text-center">
              <div class="inline-flex items-center gap-1 font-bold">
                <span
                  :class="[
                    student.attendanceRate && student.attendanceRate >= 90
                      ? 'text-emerald-600 dark:text-emerald-400'
                      : student.attendanceRate && student.attendanceRate >= 75
                        ? 'text-amber-600 dark:text-amber-400'
                        : 'text-rose-600 dark:text-rose-400'
                  ]"
                >
                  {{ student.attendanceRate }}%
                </span>
              </div>
            </td>

            <!-- Column 7: Tuition Balance -->
            <td class="py-3.5 px-4 text-right">
              <div class="flex flex-col items-end">
                <span
                  :class="[
                    'font-mono font-bold',
                    student.tuitionStatus === 'PAID'
                      ? 'text-emerald-600 dark:text-emerald-400'
                      : student.tuitionStatus === 'PENDING'
                        ? 'text-amber-600 dark:text-amber-400'
                        : 'text-rose-600 dark:text-rose-400'
                  ]"
                >
                  {{ student.balance === 0 ? '$0 (Paid)' : `$${student.balance}` }}
                </span>
                <span class="text-[10px] text-slate-400 uppercase font-semibold">
                  {{ student.tuitionStatus }}
                </span>
              </div>
            </td>

            <!-- Column 8: Quick Action -->
            <td class="py-3.5 px-4 text-center">
              <button
                type="button"
                class="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                title="View student profile"
              >
                <UIcon name="i-lucide-chevron-right" class="w-4 h-4" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Empty State -->
      <div
        v-if="students.length === 0"
        class="py-16 px-4 flex flex-col items-center justify-center text-center space-y-2"
      >
        <div class="w-12 h-12 rounded-2xl bg-slate-100 dark:bg-slate-800 text-slate-400 flex items-center justify-center mb-2">
          <UIcon name="i-lucide-users-round" class="w-6 h-6" />
        </div>
        <h4 class="text-sm font-bold text-slate-800 dark:text-slate-200">
          No students match the current filters
        </h4>
        <p class="text-xs text-slate-400 max-w-sm">
          Try clearing your search term, selecting a different course, or resetting status filters.
        </p>
      </div>
    </div>
  </div>
</template>
