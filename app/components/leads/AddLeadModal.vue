<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useCourses } from '~/composables/useCourses'
import { useLeads } from '~/composables/useLeads'

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'created'): void
}>()

const { courses } = useCourses()
const { addLead } = useLeads()

// Form state
const form = reactive({
  name: '',
  countryCode: '+82',
  phone: '',
  courseId: '',
  preferredStartDate: '',
  preferredDays: '',
  preferredTime: '',
  source: 'Instagram',
  assignedManager: 'David Miller',
  notes: ''
})

const showAdvanced = ref(false)
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

const sources = [
  'Instagram Ad',
  'Walk-in',
  'KakaoTalk Inquiry',
  'Website Form',
  'Student Referral',
  'Flyer / Banner'
]

const timeSlots = [
  'Morning (09:00 - 12:00)',
  'Afternoon (13:00 - 17:00)',
  'Evening (18:00 - 21:00)',
  'Weekend Intensive'
]

const managers = [
  'Sarah Jenkins (Director)',
  'David Miller (Academic Manager)',
  'Michael Chang (Branch Director)',
  'Elena Rostova (Senior Teacher)'
]

const isFormValid = computed(() => {
  return form.name.trim().length >= 2 &&
    form.phone.trim().length >= 7 &&
    form.courseId.trim().length > 0
})

const closeModal = () => {
  emit('update:modelValue', false)
  errorMessage.value = ''
  showSuccessBanner.value = false
}

const resetForm = () => {
  form.name = ''
  form.countryCode = '+82'
  form.phone = ''
  form.courseId = ''
  form.preferredStartDate = ''
  form.preferredDays = ''
  form.preferredTime = ''
  form.source = 'Instagram Ad'
  form.assignedManager = 'David Miller'
  form.notes = ''
  errorMessage.value = ''
  showAdvanced.value = false
}

const handlePhoneInput = (e: Event) => {
  const target = e.target as HTMLInputElement
  let val = target.value.replace(/[^0-9-]/g, '')

  // Auto-format Korean standard mobile 010-XXXX-XXXX if entered without dashes
  if (form.countryCode === '+82' && !val.includes('-')) {
    if (val.length > 3 && val.length <= 7) {
      val = `${val.slice(0, 3)}-${val.slice(3)}`
    } else if (val.length > 7) {
      val = `${val.slice(0, 3)}-${val.slice(3, 7)}-${val.slice(7, 11)}`
    }
  }

  form.phone = val
}

const handleSubmit = async () => {
  errorMessage.value = ''

  if (!form.name.trim()) {
    errorMessage.value = 'Full Name is required.'
    return
  }

  if (!form.phone.trim()) {
    errorMessage.value = 'Phone Number is required.'
    return
  }

  if (!form.courseId) {
    errorMessage.value = 'Please select an Intended Course.'
    return
  }

  isSubmitting.value = true

  try {
    const formattedPhone = form.phone.startsWith('+')
      ? form.phone
      : `${form.countryCode} ${form.phone}`

    addLead({
      name: form.name,
      phone: formattedPhone,
      courseId: form.courseId,
      source: form.source,
      preferredStartDate: form.preferredStartDate || undefined,
      preferredTime: form.preferredTime || undefined,
      assignedManager: form.assignedManager || undefined,
      notes: form.notes || undefined
    })

    showSuccessBanner.value = true

    setTimeout(() => {
      resetForm()
      closeModal()
      isSubmitting.value = false
      emit('created')
    }, 600)
  } catch (err) {
    errorMessage.value = 'Failed to create lead. Please try again.'
    isSubmitting.value = false
  }
}
</script>

<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition-opacity duration-250 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-200 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="modelValue"
        class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs overflow-y-auto"
        @click.self="closeModal"
      >
        <div
          class="w-full max-w-lg rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-2xl overflow-hidden my-8"
          role="dialog"
          aria-modal="true"
          aria-labelledby="modal-title"
        >
          <!-- Modal Header -->
          <div class="px-6 py-5 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 dark:bg-blue-950/60 dark:text-blue-400 flex items-center justify-center ring-1 ring-blue-500/20">
                <UIcon name="i-lucide-user-plus" class="w-5 h-5" />
              </div>
              <div>
                <h3 id="modal-title" class="text-base font-bold text-slate-900 dark:text-white tracking-tight">
                  Add New Lead
                </h3>
                <p class="text-xs text-slate-500 dark:text-slate-400">
                  New leads are automatically placed in the <strong class="text-blue-600 dark:text-blue-400 font-semibold">Cold</strong> column.
                </p>
              </div>
            </div>

            <button
              type="button"
              class="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              aria-label="Close dialog"
              @click="closeModal"
            >
              <UIcon name="i-lucide-x" class="w-5 h-5" />
            </button>
          </div>

          <!-- Success Alert -->
          <div
            v-if="showSuccessBanner"
            class="mx-6 mt-4 p-3 rounded-xl bg-emerald-50 text-emerald-800 dark:bg-emerald-950/50 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 flex items-center gap-2 text-xs font-semibold"
          >
            <UIcon name="i-lucide-check-circle-2" class="w-4 h-4 text-emerald-600 shrink-0" />
            <span>Lead successfully created and added to Cold column!</span>
          </div>

          <!-- Error Alert -->
          <div
            v-if="errorMessage"
            class="mx-6 mt-4 p-3 rounded-xl bg-rose-50 text-rose-800 dark:bg-rose-950/50 dark:text-rose-300 border border-rose-200 dark:border-rose-800 flex items-center gap-2 text-xs font-medium"
          >
            <UIcon name="i-lucide-alert-circle" class="w-4 h-4 text-rose-600 shrink-0" />
            <span>{{ errorMessage }}</span>
          </div>

          <!-- Form Body -->
          <form class="p-6 space-y-4" @submit.prevent="handleSubmit">
            <!-- Full Name (Required) -->
            <div>
              <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
                Full Name <span class="text-rose-500">*</span>
              </label>
              <div class="relative">
                <input
                  v-model="form.name"
                  type="text"
                  placeholder="e.g. Min-jun Kim or Sarah Connor"
                  required
                  class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950 text-sm text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 transition-all"
                />
              </div>
            </div>

            <!-- Phone Number (Required, with country code helper) -->
            <div>
              <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
                Phone Number <span class="text-rose-500">*</span>
              </label>
              <div class="flex items-center gap-2">
                <!-- Country Prefix Select -->
                <select
                  v-model="form.countryCode"
                  class="px-2.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950 text-xs font-medium text-slate-700 dark:text-slate-300 focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 shrink-0"
                >
                  <option v-for="c in countryCodes" :key="c.value" :value="c.value">
                    {{ c.label }}
                  </option>
                </select>

                <!-- Phone Input -->
                <input
                  v-model="form.phone"
                  type="tel"
                  placeholder="010-1234-5678 or 10-1234-5678"
                  required
                  class="flex-1 px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950 text-sm font-mono text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 transition-all"
                  @input="handlePhoneInput"
                />
              </div>
              <span class="text-[11px] text-slate-400 dark:text-slate-500 mt-1 block">
                Supports Korean mobile (010) and international formats with area codes.
              </span>
            </div>

            <!-- Intended Course (Required, DYNAMIC from Settings) -->
            <div>
              <div class="flex items-center justify-between mb-1.5">
                <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300">
                  Intended Course <span class="text-rose-500">*</span>
                </label>
                <NuxtLink
                  to="/settings/courses"
                  target="_blank"
                  class="text-[11px] text-primary-600 hover:text-primary-700 dark:text-primary-400 font-medium inline-flex items-center gap-1"
                >
                  <span>Manage in Settings</span>
                  <UIcon name="i-lucide-external-link" class="w-3 h-3" />
                </NuxtLink>
              </div>

              <select
                v-model="form.courseId"
                required
                class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950 text-sm text-slate-900 dark:text-white focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 transition-all"
              >
                <option value="" disabled>-- Select Intended Course --</option>
                <option
                  v-for="course in courses"
                  :key="course.id"
                  :value="course.id"
                >
                  {{ course.name }} ({{ course.level }}) — {{ course.currency || '$' }}{{ course.price }}/mo
                </option>
              </select>
            </div>

            <!-- Expandable Optional Fields Toggle -->
            <div class="pt-2 border-t border-slate-100 dark:border-slate-800">
              <button
                type="button"
                class="flex items-center justify-between w-full py-1.5 text-xs font-semibold text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200 focus:outline-hidden transition-colors"
                @click="showAdvanced = !showAdvanced"
              >
                <span>Additional Information (Optional)</span>
                <UIcon
                  :name="showAdvanced ? 'i-lucide-chevron-up' : 'i-lucide-chevron-down'"
                  class="w-4 h-4"
                />
              </button>
            </div>

            <!-- Optional Fields Section -->
            <div v-if="showAdvanced" class="space-y-3 pt-2">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <!-- Preferred Start Date -->
                <div>
                  <label class="block text-[11px] font-medium text-slate-600 dark:text-slate-400 mb-1">
                    Preferred Start Date
                  </label>
                  <input
                    v-model="form.preferredStartDate"
                    type="date"
                    class="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950 text-xs text-slate-900 dark:text-white focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500"
                  />
                </div>

                <!-- Preferred Time Slot -->
                <div>
                  <label class="block text-[11px] font-medium text-slate-600 dark:text-slate-400 mb-1">
                    Preferred Time
                  </label>
                  <select
                    v-model="form.preferredTime"
                    class="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950 text-xs text-slate-900 dark:text-white focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500"
                  >
                    <option value="">Any Time</option>
                    <option v-for="t in timeSlots" :key="t" :value="t">{{ t }}</option>
                  </select>
                </div>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <!-- Lead Source -->
                <div>
                  <label class="block text-[11px] font-medium text-slate-600 dark:text-slate-400 mb-1">
                    Inquiry Source
                  </label>
                  <select
                    v-model="form.source"
                    class="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950 text-xs text-slate-900 dark:text-white focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500"
                  >
                    <option v-for="s in sources" :key="s" :value="s">{{ s }}</option>
                  </select>
                </div>

                <!-- Assigned Manager -->
                <div>
                  <label class="block text-[11px] font-medium text-slate-600 dark:text-slate-400 mb-1">
                    Assigned Manager
                  </label>
                  <select
                    v-model="form.assignedManager"
                    class="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950 text-xs text-slate-900 dark:text-white focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500"
                  >
                    <option v-for="m in managers" :key="m" :value="m">{{ m }}</option>
                  </select>
                </div>
              </div>

              <!-- Notes -->
              <div>
                <label class="block text-[11px] font-medium text-slate-600 dark:text-slate-400 mb-1">
                  Counseling Notes / Goals
                </label>
                <textarea
                  v-model="form.notes"
                  rows="2"
                  placeholder="e.g. Needs score by December, prefers native speaker teacher..."
                  class="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950 text-xs text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500"
                />
              </div>
            </div>

            <!-- Form Actions -->
            <div class="pt-4 border-t border-slate-100 dark:border-slate-800 flex items-center justify-end gap-3">
              <button
                type="button"
                class="px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-800 text-xs font-semibold text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors focus:outline-hidden"
                @click="closeModal"
              >
                Cancel
              </button>

              <button
                type="submit"
                :disabled="!isFormValid || isSubmitting"
                :class="[
                  'px-5 py-2.5 rounded-xl text-xs font-bold text-white shadow-xs transition-all flex items-center gap-2 focus:outline-hidden',
                  isFormValid && !isSubmitting
                    ? 'bg-primary-600 hover:bg-primary-700 cursor-pointer shadow-primary-600/20'
                    : 'bg-slate-300 dark:bg-slate-800 text-slate-400 dark:text-slate-600 cursor-not-allowed'
                ]"
              >
                <UIcon
                  v-if="isSubmitting"
                  name="i-lucide-loader-2"
                  class="w-4 h-4 animate-spin"
                />
                <UIcon
                  v-else
                  name="i-lucide-check"
                  class="w-4 h-4"
                />
                <span>{{ isSubmitting ? 'Saving Lead...' : 'Save Lead' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>
