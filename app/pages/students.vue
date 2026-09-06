<script setup lang="ts">
useSeoMeta({
  title: 'All Students • Education Center CRM',
  description: 'Enrolled Students Directory and Records'
})
</script>

<template>
  <div class="h-full min-h-[400px] rounded-2xl border-2 border-dashed border-slate-200 dark:border-slate-800/80 bg-white/50 dark:bg-slate-900/40 p-8 sm:p-12 flex flex-col items-center justify-center text-center">
    <div class="w-14 h-14 rounded-2xl bg-primary-50 dark:bg-primary-950/50 text-primary-600 dark:text-primary-400 flex items-center justify-center mb-4 ring-1 ring-primary-500/20 shadow-xs">
      <UIcon name="i-lucide-user-check" class="w-7 h-7" />
    </div>
    <h2 class="text-xl font-bold text-slate-900 dark:text-white tracking-tight">
      All Students
    </h2>
    <p class="mt-1 text-sm text-slate-500 dark:text-slate-400 max-w-sm">
      Main content placeholder. Enrolled student records, attendance histories, guardian contacts, and individual academic profiles will be managed here.
    </p>
  </div>
</template>
