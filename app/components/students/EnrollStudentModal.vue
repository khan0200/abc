<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useCourses } from '~/composables/useCourses'
import { useStudents } from '~/composables/useStudents'

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'enrolled'): void
}>()

const { courses } = useCourses()
const { enrollStudent } = useStudents()

const form = reactive({
  name: '',
  email: '',
  countryCode: '+82',
  phone: '',
  courseId: '',
  groupName: '',
  branch: 'Central Campus',
  guardianName: '',
  guardianPhone: '',
  notes: ''
})

const errorMessage = ref('')
const isSubmitting = ref(false)
const showSuccessBanner = ref(false)

const countryCodes = [
  { label: '🇰🇷 Korea (+82)', value: '+82' },
  { label: '🇺🇸 USA (+1)', value: '+1' },
  { label: '🇺🇿 Uzbekistan (+998)', value: '+998' },
  { label: '🇨🇳 China (+86)', value: '+86' },
  { label: '🇯🇵 Japan (+81)', value: '+81' },
  { label: '🇬🇧 UK (+44)', value: '+44' }
]

const branches = [
  'Central Campus',
  'Downtown Branch'
]

const isFormValid = computed(() => {
  return form.name.trim().length >= 2 &&
    form.email.trim().includes('@') &&
    form.phone.trim().length >= 6 &&
    form.courseId.trim().length > 0 &&
    form.groupName.trim().length > 0
})

const closeModal = () => {
  emit('update:modelValue', false)
  errorMessage.value = ''
  showSuccessBanner.value = false
}

const resetForm = () => {
  form.name = ''
  form.email = ''
  form.countryCode = '+82'
  form.phone = ''
  form.courseId = ''
  form.groupName = ''
  form.branch = 'Central Campus'
  form.guardianName = ''
  form.guardianPhone = ''
  form.notes = ''
}

const handleSubmit = async () => {
  if (!isFormValid.value) {
    errorMessage.value = 'Please fill in all required fields marked with *'
    return
  }

  isSubmitting.value = true
  errorMessage.value = ''

  try {
    const fullPhone = form.phone.startsWith('+') ? form.phone : `${form.countryCode} ${form.phone}`

    enrollStudent({
      name: form.name,
      email: form.email,
      phone: fullPhone,
      courseId: form.courseId,
      groupName: form.groupName,
      branch: form.branch,
      guardianName: form.guardianName || undefined,
      guardianPhone: form.guardianPhone || undefined,
      notes: form.notes || undefined
    })

    showSuccessBanner.value = true
    setTimeout(() => {
      resetForm()
      closeModal()
      emit('enrolled')
      isSubmitting.value = false
    }, 800)
  } catch (err: any) {
    errorMessage.value = err?.message || 'Failed to enroll student. Please try again.'
    isSubmitting.value = false
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
        v-if="modelValue"
        class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-xs overflow-y-auto"
        @click.self="closeModal"
      >
        <div
          class="relative w-full max-w-xl my-8 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200"
        >
          <!-- Header -->
          <div class="px-6 py-4 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between bg-slate-50/50 dark:bg-slate-950/30">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-primary-50 text-primary-600 dark:bg-primary-950/80 dark:text-primary-400 flex items-center justify-center ring-1 ring-primary-500/20">
                <UIcon name="i-lucide-user-plus" class="w-5 h-5" />
              </div>
              <div>
                <h3 class="text-base font-bold text-slate-900 dark:text-white">
                  Enroll New Student
                </h3>
                <p class="text-xs text-slate-500 dark:text-slate-400">
                  Register a student into center roster and assign to cohort.
                </p>
              </div>
            </div>

            <button
              type="button"
              class="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              @click="closeModal"
            >
              <UIcon name="i-lucide-x" class="w-5 h-5" />
            </button>
          </div>

          <!-- Success Banner -->
          <div
            v-if="showSuccessBanner"
            class="mx-6 mt-4 p-3.5 rounded-xl bg-emerald-50 dark:bg-emerald-950/50 border border-emerald-200 dark:border-emerald-800 text-emerald-800 dark:text-emerald-200 text-xs flex items-center gap-2 font-medium animate-in fade-in"
          >
            <UIcon name="i-lucide-check-circle" class="w-4 h-4 text-emerald-600 shrink-0" />
            <span>Student enrolled successfully! Adding to roster...</span>
          </div>

          <!-- Error Alert -->
          <div
            v-if="errorMessage"
            class="mx-6 mt-4 p-3 rounded-xl bg-rose-50 dark:bg-rose-950/50 border border-rose-200 dark:border-rose-800 text-rose-800 dark:text-rose-200 text-xs flex items-center gap-2 font-medium"
          >
            <UIcon name="i-lucide-alert-circle" class="w-4 h-4 text-rose-600 shrink-0" />
            <span>{{ errorMessage }}</span>
          </div>

          <!-- Form Body -->
          <form class="p-6 space-y-4 max-h-[75vh] overflow-y-auto" @submit.prevent="handleSubmit">
            <!-- Full Name & Email -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div class="space-y-1.5">
                <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300">
                  Full Name <span class="text-rose-500">*</span>
                </label>
                <div class="relative">
                  <UIcon name="i-lucide-user" class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    v-model="form.name"
                    type="text"
                    required
                    placeholder="e.g. Min-jun Kim"
                    class="w-full pl-9 pr-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950 text-xs text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 transition-all"
                  />
                </div>
              </div>

              <div class="space-y-1.5">
                <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300">
                  Email Address <span class="text-rose-500">*</span>
                </label>
                <div class="relative">
                  <UIcon name="i-lucide-mail" class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    v-model="form.email"
                    type="email"
                    required
                    placeholder="student@example.com"
                    class="w-full pl-9 pr-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950 text-xs text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 transition-all"
                  />
                </div>
              </div>
            </div>

            <!-- Phone Number with Country Code -->
            <div class="space-y-1.5">
              <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300">
                Phone Number <span class="text-rose-500">*</span>
              </label>
              <div class="flex gap-2">
                <select
                  v-model="form.countryCode"
                  class="w-36 px-2.5 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950 text-xs font-medium text-slate-700 dark:text-slate-300 focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500"
                >
                  <option v-for="c in countryCodes" :key="c.value" :value="c.value">
                    {{ c.label }}
                  </option>
                </select>

                <div class="relative flex-1">
                  <UIcon name="i-lucide-phone" class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    v-model="form.phone"
                    type="tel"
                    required
                    placeholder="010-1234-5678"
                    class="w-full pl-9 pr-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950 text-xs text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 transition-all font-mono"
                  />
                </div>
              </div>
            </div>

            <!-- Course Selection (Dynamic from Settings) & Group -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div class="space-y-1.5">
                <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300">
                  Enrolled Course <span class="text-rose-500">*</span>
                </label>
                <select
                  v-model="form.courseId"
                  required
                  class="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950 text-xs font-medium text-slate-700 dark:text-slate-300 focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500"
                >
                  <option value="" disabled>Select Course from Settings</option>
                  <option v-for="c in courses" :key="c.id" :value="c.id">
                    {{ c.name }} ({{ c.level }}) — {{ c.currency || '$' }}{{ c.price }}
                  </option>
                </select>
              </div>

              <div class="space-y-1.5">
                <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300">
                  Cohort / Group Name <span class="text-rose-500">*</span>
                </label>
                <div class="relative">
                  <UIcon name="i-lucide-users" class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    v-model="form.groupName"
                    type="text"
                    required
                    placeholder="e.g. IELTS Morning A (Mon/Wed)"
                    class="w-full pl-9 pr-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950 text-xs text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 transition-all"
                  />
                </div>
              </div>
            </div>

            <!-- Campus Branch -->
            <div class="space-y-1.5">
              <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300">
                Campus Branch
              </label>
              <select
                v-model="form.branch"
                class="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950 text-xs font-medium text-slate-700 dark:text-slate-300 focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500"
              >
                <option v-for="b in branches" :key="b" :value="b">
                  {{ b }}
                </option>
              </select>
            </div>

            <!-- Guardian Details (Optional) -->
            <div class="pt-2 border-t border-slate-100 dark:border-slate-800/80">
              <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-2">
                Guardian / Emergency Contact (Optional)
              </span>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div class="space-y-1">
                  <label class="block text-[11px] font-medium text-slate-600 dark:text-slate-400">
                    Guardian Name
                  </label>
                  <input
                    v-model="form.guardianName"
                    type="text"
                    placeholder="e.g. Hyun-woo Kim"
                    class="w-full px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950 text-xs text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500"
                  />
                </div>

                <div class="space-y-1">
                  <label class="block text-[11px] font-medium text-slate-600 dark:text-slate-400">
                    Guardian Phone
                  </label>
                  <input
                    v-model="form.guardianPhone"
                    type="tel"
                    placeholder="010-0000-0000"
                    class="w-full px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950 text-xs text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 font-mono"
                  />
                </div>
              </div>
            </div>

            <!-- Notes -->
            <div class="space-y-1.5">
              <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300">
                Enrollment Notes
              </label>
              <textarea
                v-model="form.notes"
                rows="2"
                placeholder="Academic goals, test scores, or schedule preferences..."
                class="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950 text-xs text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 transition-all resize-none"
              />
            </div>

            <!-- Actions -->
            <div class="flex items-center justify-end gap-3 pt-4 border-t border-slate-100 dark:border-slate-800">
              <button
                type="button"
                class="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                @click="closeModal"
              >
                Cancel
              </button>

              <button
                type="submit"
                :disabled="!isFormValid || isSubmitting"
                class="inline-flex items-center gap-2 px-5 py-2 rounded-xl bg-primary-600 hover:bg-primary-700 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed text-white text-xs font-bold shadow-sm shadow-primary-600/30 transition-all cursor-pointer"
              >
                <UIcon v-if="isSubmitting" name="i-lucide-loader-2" class="w-4 h-4 animate-spin" />
                <UIcon v-else name="i-lucide-user-check" class="w-4 h-4" />
                <span>{{ isSubmitting ? 'Enrolling...' : 'Confirm Enrollment' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>
