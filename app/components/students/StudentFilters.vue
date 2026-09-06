<script setup lang="ts">
import { computed } from 'vue'
import { useStudents } from '~/composables/useStudents'
import { useCourses } from '~/composables/useCourses'

const {
  searchQuery,
  selectedCourse,
  selectedStatus,
  selectedBranch,
  resetFilters
} = useStudents()

const { courses } = useCourses()

const hasActiveFilters = computed(() => {
  return !!searchQuery.value ||
    selectedCourse.value !== 'all' ||
    selectedStatus.value !== 'all' ||
    selectedBranch.value !== 'all'
})
</script>

<template>
  <div class="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-2xs space-y-3">
    <!-- Top Row: Search and Quick Filter Dropdowns -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-12 gap-3">
      <!-- Search Input (Span 5 columns) -->
      <div class="lg:col-span-5 relative">
        <UIcon
          name="i-lucide-search"
          class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2"
        />
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search by student name, phone, ID, or email..."
          class="w-full pl-10 pr-9 py-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-950 text-xs text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 transition-all"
        />
        <button
          v-if="searchQuery"
          type="button"
          class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-0.5"
          @click="searchQuery = ''"
        >
          <UIcon name="i-lucide-x" class="w-3.5 h-3.5" />
        </button>
      </div>

      <!-- Course Filter (Span 3 columns, Dynamic from Settings) -->
      <div class="lg:col-span-3">
        <select
          v-model="selectedCourse"
          class="w-full px-3 py-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-950 text-xs font-medium text-slate-700 dark:text-slate-300 focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 truncate"
        >
          <option value="all">All Enrolled Courses</option>
          <option v-for="course in courses" :key="course.id" :value="course.id">
            {{ course.name }} ({{ course.level }})
          </option>
        </select>
      </div>

      <!-- Status Filter (Span 2 columns) -->
      <div class="lg:col-span-2">
        <select
          v-model="selectedStatus"
          class="w-full px-3 py-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-950 text-xs font-medium text-slate-700 dark:text-slate-300 focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500"
        >
          <option value="all">All Statuses</option>
          <option value="ACTIVE">🟢 Active</option>
          <option value="ON_LEAVE">🟡 On Leave</option>
          <option value="GRADUATED">🔵 Graduated</option>
          <option value="INACTIVE">⚪ Inactive</option>
        </select>
      </div>

      <!-- Branch Filter (Span 2 columns) -->
      <div class="lg:col-span-2">
        <select
          v-model="selectedBranch"
          class="w-full px-3 py-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-950 text-xs font-medium text-slate-700 dark:text-slate-300 focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500"
        >
          <option value="all">All Campuses</option>
          <option value="Central Campus">Central Campus</option>
          <option value="Downtown Branch">Downtown Branch</option>
        </select>
      </div>
    </div>

    <!-- Active Filters Row & Reset Action -->
    <div
      v-if="hasActiveFilters"
      class="flex items-center justify-between pt-2 border-t border-slate-100 dark:border-slate-800/80 text-xs"
    >
      <div class="flex items-center gap-2 flex-wrap">
        <span class="text-slate-400 font-medium text-[11px]">Filtered By:</span>

        <span
          v-if="searchQuery"
          class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-[11px] text-slate-700 dark:text-slate-300"
        >
          Keyword: "{{ searchQuery }}"
          <button type="button" @click="searchQuery = ''"><UIcon name="i-lucide-x" class="w-3 h-3" /></button>
        </span>

        <span
          v-if="selectedCourse !== 'all'"
          class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-primary-50 dark:bg-primary-950 text-primary-700 dark:text-primary-300 text-[11px] font-medium"
        >
          Course
          <button type="button" @click="selectedCourse = 'all'"><UIcon name="i-lucide-x" class="w-3 h-3" /></button>
        </span>

        <span
          v-if="selectedStatus !== 'all'"
          class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-[11px] text-slate-700 dark:text-slate-300 font-medium"
        >
          Status: {{ selectedStatus }}
          <button type="button" @click="selectedStatus = 'all'"><UIcon name="i-lucide-x" class="w-3 h-3" /></button>
        </span>

        <span
          v-if="selectedBranch !== 'all'"
          class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-[11px] text-slate-700 dark:text-slate-300 font-medium"
        >
          {{ selectedBranch }}
          <button type="button" @click="selectedBranch = 'all'"><UIcon name="i-lucide-x" class="w-3 h-3" /></button>
        </span>
      </div>

      <button
        type="button"
        class="text-[11px] font-semibold text-rose-600 hover:text-rose-700 dark:text-rose-400 inline-flex items-center gap-1"
        @click="resetFilters"
      >
        <UIcon name="i-lucide-rotate-ccw" class="w-3 h-3" />
        <span>Reset Filters</span>
      </button>
    </div>
  </div>
</template>
