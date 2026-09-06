<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useSidebar } from '~/composables/useSidebar'

const route = useRoute()
const { toggleMobile, navItems } = useSidebar()

const currentItem = computed(() => {
  if (route.path === '/') {
    return navItems.find(item => item.to === '/')
  }
  return navItems.find(item => item.to !== '/' && (route.path === item.to || route.path.startsWith(`${item.to}/`)))
})

const pageTitle = computed(() => currentItem.value?.label || 'Overview')
</script>

<template>
  <header class="h-16 sticky top-0 z-30 flex items-center justify-between px-4 sm:px-6 bg-white/80 dark:bg-slate-950/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800/80">
    <!-- Left: Mobile Toggle & Page Title/Breadcrumb -->
    <div class="flex items-center gap-3 sm:gap-4 min-w-0">
      <!-- Mobile Sidebar Toggle -->
      <button
        type="button"
        class="lg:hidden p-2 rounded-xl text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800/60 focus:outline-hidden transition-colors"
        aria-label="Open sidebar menu"
        @click="toggleMobile"
      >
        <UIcon
          name="i-lucide-menu"
          class="w-5 h-5"
        />
      </button>

      <!-- Breadcrumb & Title Indicator -->
      <div class="flex flex-col min-w-0">
        <div class="flex items-center gap-1.5 text-xs text-slate-400 dark:text-slate-500 font-medium">
          <span>CRM</span>
          <UIcon
            name="i-lucide-chevron-right"
            class="w-3.5 h-3.5 shrink-0"
          />
          <span class="text-slate-700 dark:text-slate-300 font-semibold">{{ pageTitle }}</span>
        </div>
        <h1 class="text-base sm:text-lg font-bold text-slate-900 dark:text-white tracking-tight leading-tight truncate">
          {{ pageTitle }}
        </h1>
      </div>
    </div>

    <!-- Right: Quick Status, Dark Mode Toggle & Help -->
    <div class="flex items-center gap-2 sm:gap-3">
      <!-- Term Status Badge -->
      <div class="hidden sm:inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 dark:bg-slate-800/70 text-slate-600 dark:text-slate-300 border border-slate-200/60 dark:border-slate-700/60">
        <UIcon
          name="i-lucide-calendar"
          class="w-3.5 h-3.5 text-primary-600 dark:text-primary-400"
        />
        <span>Fall 2026 Term</span>
      </div>

      <!-- Theme Switcher -->
      <UColorModeButton />

      <!-- Notification Icon Placeholder -->
      <button
        type="button"
        class="p-2 rounded-xl text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800/60 focus:outline-hidden transition-colors relative"
        aria-label="Notifications"
      >
        <UIcon
          name="i-lucide-bell"
          class="w-5 h-5"
        />
        <span class="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-primary-600" />
      </button>
    </div>
  </header>
</template>
