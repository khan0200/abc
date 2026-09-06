<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()

useSeoMeta({
  title: 'Settings • Education Center CRM',
  description: 'Academy Settings, Staff, Courses, and Payment Configurations'
})

const tabs = [
  {
    label: 'Staff Management',
    to: '/settings/staff',
    icon: 'i-lucide-user-cog',
    badge: 'Users'
  },
  {
    label: 'Courses',
    to: '/settings/courses',
    icon: 'i-lucide-book-open',
    badge: 'Curriculum'
  },
  {
    label: 'Payment Settings',
    to: '/settings/payments',
    icon: 'i-lucide-credit-card',
    badge: 'Billing'
  }
]

const isTabActive = (to: string) => {
  return route.path === to
}
</script>

<template>
  <div class="space-y-6">
    <!-- Settings Section Header & Sub-navigation Tabs -->
    <div class="border-b border-slate-200 dark:border-slate-800 pb-4">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-4">
        <div>
          <h2 class="text-xl font-bold text-slate-900 dark:text-white tracking-tight">
            Settings & Configurations
          </h2>
          <p class="text-xs sm:text-sm text-slate-500 dark:text-slate-400">
            Configure center staff accounts, course catalog pricing, and payment collection settings.
          </p>
        </div>
      </div>

      <!-- Tab Navigation -->
      <nav class="flex items-center gap-2 overflow-x-auto pb-1" aria-label="Settings Subsections">
        <NuxtLink
          v-for="tab in tabs"
          :key="tab.to"
          :to="tab.to"
          :class="[
            'flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs sm:text-sm font-medium transition-all shrink-0',
            isTabActive(tab.to)
              ? 'bg-primary-600 text-white font-semibold shadow-xs'
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800/60'
          ]"
        >
          <UIcon :name="tab.icon" class="w-4 h-4 shrink-0" />
          <span>{{ tab.label }}</span>
        </NuxtLink>
      </nav>
    </div>

    <!-- Nested Tab Content -->
    <NuxtPage />
  </div>
</template>
