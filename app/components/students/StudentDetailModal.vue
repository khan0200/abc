<script setup lang="ts">
import { ref } from 'vue'
import type { Student, StudentStatus } from '~/types/student'
import { useStudents } from '~/composables/useStudents'

const props = defineProps<{
  student: Student | null
  isOpen: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const { updateStudentStatus } = useStudents()

const copiedField = ref<string | null>(null)

const copyText = async (field: string, text: string) => {
  try {
    await navigator.clipboard.writeText(text)
    copiedField.value = field
    setTimeout(() => {
      copiedField.value = null
    }, 1500)
  } catch (err) {
    console.error('Failed to copy', err)
  }
}

const handleStatusChange = (newStatus: StudentStatus) => {
  if (props.student) {
    updateStudentStatus(props.student.id, newStatus)
  }
}
</script>

<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition-opacity duration-200 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-150 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="isOpen && student"
        class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-xs overflow-y-auto"
        @click.self="emit('close')"
      >
        <div
          class="relative w-full max-w-lg my-8 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200"
        >
          <!-- Header Banner with Avatar and Student ID -->
          <div class="p-6 border-b border-slate-100 dark:border-slate-800 bg-slate-50/70 dark:bg-slate-950/40">
            <div class="flex items-start justify-between gap-4">
              <div class="flex items-center gap-4">
                <div class="w-14 h-14 rounded-2xl bg-primary-100 text-primary-700 dark:bg-primary-950 dark:text-primary-300 font-bold text-xl flex items-center justify-center ring-2 ring-primary-500/20 shrink-0">
                  {{ student.name.charAt(0).toUpperCase() }}
                </div>
                <div>
                  <div class="flex items-center gap-2">
                    <h3 class="text-lg font-bold text-slate-900 dark:text-white">
                      {{ student.name }}
                    </h3>
                    <span class="px-2 py-0.5 rounded-md text-xs font-mono font-bold bg-slate-200/70 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
                      {{ student.studentId }}
                    </span>
                  </div>
                  <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                    Enrolled on {{ student.enrolledAt }} • {{ student.branch }}
                  </p>
                </div>
              </div>

              <button
                type="button"
                class="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                @click="emit('close')"
              >
                <UIcon
                  name="i-lucide-x"
                  class="w-5 h-5"
                />
              </button>
            </div>

            <!-- Status Changer Segmented Control -->
            <div class="mt-4 pt-4 border-t border-slate-200/60 dark:border-slate-800/80">
              <span class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-2">
                Enrollment Status:
              </span>
              <div class="grid grid-cols-4 gap-1.5 p-1 rounded-xl bg-slate-200/60 dark:bg-slate-800/80 text-xs font-semibold">
                <button
                  type="button"
                  :class="[
                    'py-1.5 rounded-lg transition-all text-center',
                    student.status === 'ACTIVE'
                      ? 'bg-emerald-600 text-white shadow-xs'
                      : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                  ]"
                  @click="handleStatusChange('ACTIVE')"
                >
                  Active
                </button>
                <button
                  type="button"
                  :class="[
                    'py-1.5 rounded-lg transition-all text-center',
                    student.status === 'ON_LEAVE'
                      ? 'bg-amber-500 text-white shadow-xs'
                      : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                  ]"
                  @click="handleStatusChange('ON_LEAVE')"
                >
                  On Leave
                </button>
                <button
                  type="button"
                  :class="[
                    'py-1.5 rounded-lg transition-all text-center',
                    student.status === 'GRADUATED'
                      ? 'bg-blue-600 text-white shadow-xs'
                      : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                  ]"
                  @click="handleStatusChange('GRADUATED')"
                >
                  Graduated
                </button>
                <button
                  type="button"
                  :class="[
                    'py-1.5 rounded-lg transition-all text-center',
                    student.status === 'INACTIVE'
                      ? 'bg-slate-600 text-white shadow-xs'
                      : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                  ]"
                  @click="handleStatusChange('INACTIVE')"
                >
                  Inactive
                </button>
              </div>
            </div>
          </div>

          <!-- Body Content -->
          <div class="p-6 space-y-5 max-h-[60vh] overflow-y-auto text-xs">
            <!-- Academic & Group Info -->
            <div class="grid grid-cols-2 gap-3">
              <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/40">
                <span class="text-slate-400 text-[11px] block">Course Program</span>
                <span class="font-bold text-slate-900 dark:text-white text-sm mt-0.5 block">
                  {{ student.courseName }}
                </span>
                <span class="text-[11px] text-primary-600 dark:text-primary-400 font-medium">
                  {{ student.groupName }}
                </span>
              </div>

              <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/40">
                <span class="text-slate-400 text-[11px] block">Tuition & Attendance</span>
                <div class="flex items-baseline justify-between mt-0.5">
                  <span
                    :class="[
                      'font-bold text-sm',
                      student.tuitionStatus === 'PAID'
                        ? 'text-emerald-600 dark:text-emerald-400'
                        : student.tuitionStatus === 'PENDING'
                          ? 'text-amber-600 dark:text-amber-400'
                          : 'text-rose-600 dark:text-rose-400'
                    ]"
                  >
                    {{ student.balance === 0 ? '$0 (Paid)' : `$${student.balance} Due` }}
                  </span>
                  <span class="font-semibold text-slate-700 dark:text-slate-300">
                    {{ student.attendanceRate ?? 100 }}% Attend
                  </span>
                </div>
                <div class="w-full bg-slate-200 dark:bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
                  <div
                    class="bg-emerald-500 h-full rounded-full"
                    :style="{ width: `${student.attendanceRate ?? 100}%` }"
                  />
                </div>
              </div>
            </div>

            <!-- Contact Information -->
            <div class="space-y-2">
              <h4 class="font-bold text-slate-700 dark:text-slate-300 text-[11px] uppercase tracking-wider">
                Direct Contact
              </h4>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                <!-- Phone -->
                <div class="flex items-center justify-between p-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
                  <div class="flex items-center gap-2">
                    <UIcon
                      name="i-lucide-phone"
                      class="w-4 h-4 text-slate-400 shrink-0"
                    />
                    <span class="font-mono font-medium text-slate-800 dark:text-slate-200">{{ student.phone }}</span>
                  </div>
                  <button
                    type="button"
                    class="text-xs text-primary-600 hover:text-primary-700 font-medium"
                    @click="copyText('phone', student.phone)"
                  >
                    {{ copiedField === 'phone' ? 'Copied!' : 'Copy' }}
                  </button>
                </div>

                <!-- Email -->
                <div class="flex items-center justify-between p-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
                  <div class="flex items-center gap-2 truncate pr-2">
                    <UIcon
                      name="i-lucide-mail"
                      class="w-4 h-4 text-slate-400 shrink-0"
                    />
                    <span class="text-slate-800 dark:text-slate-200 truncate">{{ student.email }}</span>
                  </div>
                  <button
                    type="button"
                    class="text-xs text-primary-600 hover:text-primary-700 font-medium shrink-0"
                    @click="copyText('email', student.email)"
                  >
                    {{ copiedField === 'email' ? 'Copied!' : 'Copy' }}
                  </button>
                </div>
              </div>
            </div>

            <!-- Guardian / Emergency Info -->
            <div
              v-if="student.guardianName || student.guardianPhone"
              class="space-y-2"
            >
              <h4 class="font-bold text-slate-700 dark:text-slate-300 text-[11px] uppercase tracking-wider">
                Guardian / Emergency Contact
              </h4>
              <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 flex items-center justify-between">
                <div>
                  <span class="font-semibold text-slate-900 dark:text-white block">
                    {{ student.guardianName || 'Guardian' }}
                  </span>
                  <span
                    v-if="student.guardianPhone"
                    class="font-mono text-slate-500 text-[11px]"
                  >
                    {{ student.guardianPhone }}
                  </span>
                </div>
                <button
                  v-if="student.guardianPhone"
                  type="button"
                  class="text-xs text-primary-600 hover:text-primary-700 font-medium"
                  @click="copyText('guardian', student.guardianPhone)"
                >
                  {{ copiedField === 'guardian' ? 'Copied!' : 'Copy' }}
                </button>
              </div>
            </div>

            <!-- Notes Section -->
            <div
              v-if="student.notes"
              class="space-y-1.5"
            >
              <h4 class="font-bold text-slate-700 dark:text-slate-300 text-[11px] uppercase tracking-wider">
                Academic & Counselor Notes
              </h4>
              <p class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/40 text-slate-600 dark:text-slate-400 leading-relaxed">
                {{ student.notes }}
              </p>
            </div>
          </div>

          <!-- Footer -->
          <div class="px-6 py-3.5 border-t border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/30 flex items-center justify-between">
            <span class="text-[11px] text-slate-400">
              Database ID: {{ student.id }}
            </span>
            <button
              type="button"
              class="px-4 py-2 rounded-xl bg-slate-200 hover:bg-slate-300 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 text-xs font-bold transition-colors cursor-pointer"
              @click="emit('close')"
            >
              Done
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>
