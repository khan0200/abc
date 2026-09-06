<script setup lang="ts">
useSeoMeta({
  title: 'Payment Settings • Settings • Education Center CRM',
  description: 'Manage accepted payment methods, designated receivers, and quick-pick receipt notes'
})
</script>

<template>
  <div class="rounded-2xl border-2 border-dashed border-slate-200 dark:border-slate-800/80 bg-white/50 dark:bg-slate-900/40 p-8 sm:p-12 flex flex-col items-center justify-center text-center">
    <div class="w-14 h-14 rounded-2xl bg-primary-50 dark:bg-primary-950/50 text-primary-600 dark:text-primary-400 flex items-center justify-center mb-4 ring-1 ring-primary-500/20 shadow-xs">
      <UIcon
        name="i-lucide-credit-card"
        class="w-7 h-7"
      />
    </div>

    <h3 class="text-lg font-bold text-slate-900 dark:text-white tracking-tight">
      Payment Settings
    </h3>

    <p class="mt-1 text-sm text-slate-500 dark:text-slate-400 max-w-md">
      Placeholder for tuition payment parameters. Billing rules will be configured here with <strong class="text-slate-700 dark:text-slate-300">Payment Method</strong>, <strong class="text-slate-700 dark:text-slate-300">Receiver</strong>, and <strong class="text-slate-700 dark:text-slate-300">Quick Pick Notes</strong>.
    </p>

    <!-- Schema indicators matching requested fields -->
    <div class="mt-6 flex flex-wrap items-center justify-center gap-2">
      <span class="px-3 py-1 rounded-lg text-xs font-medium bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
        Field: Payment Method (Cash, Bank Card, Wire)
      </span>
      <span class="px-3 py-1 rounded-lg text-xs font-medium bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
        Field: Designated Receiver (Academy Account)
      </span>
      <span class="px-3 py-1 rounded-lg text-xs font-medium bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
        Field: Quick Pick Notes (e.g., Early Bird, Sibling)
      </span>
    </div>
  </div>
</template>
