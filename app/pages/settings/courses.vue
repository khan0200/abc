<script setup lang="ts">
import { ref } from 'vue'
import { useCourses } from '~/composables/useCourses'

useSeoMeta({
  title: 'Courses • Settings • Education Center CRM',
  description: 'Manage course curriculum, levels, and pricing'
})

const { courses, addCourse } = useCourses()

const isAddingCourse = ref(false)
const newCourse = ref({
  name: '',
  level: 'Beginner',
  price: 200,
  currency: '$',
  description: ''
})

const handleCreateCourse = () => {
  if (!newCourse.value.name.trim()) return

  addCourse({
    name: newCourse.value.name.trim(),
    level: newCourse.value.level,
    price: Number(newCourse.value.price) || 200,
    currency: newCourse.value.currency || '$',
    description: newCourse.value.description.trim() || undefined,
    isActive: true
  })

  newCourse.value = {
    name: '',
    level: 'Beginner',
    price: 200,
    currency: '$',
    description: ''
  }
  isAddingCourse.value = false
}
</script>

<template>
  <div class="space-y-6">
    <!-- Header with + Add Course Button -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
      <div>
        <h3 class="text-base font-bold text-slate-900 dark:text-white tracking-tight">
          Course Catalog & Pricing
        </h3>
        <p class="text-xs text-slate-500 dark:text-slate-400">
          Courses configured here are automatically synchronized with the <strong class="text-primary-600 dark:text-primary-400">Leads</strong> intended course dropdown.
        </p>
      </div>

      <button
        type="button"
        class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-primary-600 hover:bg-primary-700 text-white text-xs font-bold shadow-xs transition-colors self-start sm:self-auto"
        @click="isAddingCourse = !isAddingCourse"
      >
        <UIcon :name="isAddingCourse ? 'i-lucide-x' : 'i-lucide-plus'" class="w-4 h-4" />
        <span>{{ isAddingCourse ? 'Cancel' : 'Add Course' }}</span>
      </button>
    </div>

    <!-- Add Course Form (Collapsible) -->
    <div
      v-if="isAddingCourse"
      class="p-5 rounded-2xl bg-slate-50 dark:bg-slate-900/80 border border-primary-200 dark:border-primary-900/60 space-y-4"
    >
      <h4 class="text-sm font-bold text-slate-900 dark:text-white">
        Create New Course
      </h4>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div>
          <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
            Course Name *
          </label>
          <input
            v-model="newCourse.name"
            type="text"
            placeholder="e.g. SAT Math or Business Spanish"
            required
            class="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950 text-xs text-slate-900 dark:text-white focus:ring-2 focus:ring-primary-500"
          />
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
            Level / Classification
          </label>
          <input
            v-model="newCourse.level"
            type="text"
            placeholder="e.g. Intermediate or A2"
            class="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950 text-xs text-slate-900 dark:text-white focus:ring-2 focus:ring-primary-500"
          />
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
            Price ($ / month)
          </label>
          <input
            v-model="newCourse.price"
            type="number"
            placeholder="250"
            class="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950 text-xs text-slate-900 dark:text-white focus:ring-2 focus:ring-primary-500"
          />
        </div>
      </div>

      <div class="flex justify-end gap-2 pt-2">
        <button
          type="button"
          class="px-4 py-2 rounded-xl bg-primary-600 text-white text-xs font-bold hover:bg-primary-700 cursor-pointer"
          @click="handleCreateCourse"
        >
          Save Course to Catalog
        </button>
      </div>
    </div>

    <!-- Active Courses Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div
        v-for="course in courses"
        :key="course.id"
        class="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-2xs hover:shadow-xs transition-shadow flex flex-col justify-between"
      >
        <div>
          <div class="flex items-start justify-between gap-2 mb-2">
            <span class="text-[10px] font-bold px-2 py-0.5 rounded-md bg-primary-50 text-primary-700 dark:bg-primary-950 dark:text-primary-300 border border-primary-200/60 dark:border-primary-900/60">
              {{ course.level }}
            </span>
            <span class="font-bold text-sm text-slate-900 dark:text-white">
              {{ course.currency || '$' }}{{ course.price }}<span class="text-[11px] font-normal text-slate-400">/mo</span>
            </span>
          </div>

          <h4 class="font-bold text-sm text-slate-900 dark:text-white tracking-tight">
            {{ course.name }}
          </h4>
          <p v-if="course.description" class="text-xs text-slate-500 dark:text-slate-400 mt-1 line-clamp-2">
            {{ course.description }}
          </p>
        </div>

        <div class="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-[11px] text-slate-400">
          <span class="flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500" />
            Active in Leads
          </span>
          <span class="font-mono text-[10px]">ID: {{ course.id.slice(0, 10) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
