<script setup lang="ts">
import { useSidebar } from '~/composables/useSidebar'
import AppSidebar from '~/components/sidebar/AppSidebar.vue'
import AppHeader from '~/components/layout/AppHeader.vue'

const { isCollapsed } = useSidebar()
</script>

<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 flex flex-col font-sans antialiased selection:bg-primary-500 selection:text-white">
    <!-- Application Sidebar Navigation -->
    <AppSidebar />

    <!-- Application Shell Content Area -->
    <div
      :class="[
        'flex-1 flex flex-col min-h-screen transition-all duration-300 ease-in-out',
        isCollapsed ? 'lg:pl-20' : 'lg:pl-64'
      ]"
    >
      <AppHeader />

      <!-- Main Content Placeholder Area -->
      <main class="flex-1 p-4 sm:p-6 lg:p-8">
        <div class="max-w-7xl mx-auto h-full">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>
