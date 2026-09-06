<script setup lang="ts">
useSeoMeta({
  title: 'Finance • Education Center CRM',
  description: 'Tuition and Invoicing'
})
</script>

<template>
  <div class="h-full min-h-[400px] rounded-2xl border-2 border-dashed border-slate-200 dark:border-slate-800/80 bg-white/50 dark:bg-slate-900/40 p-8 sm:p-12 flex flex-col items-center justify-center text-center">
    <div class="w-14 h-14 rounded-2xl bg-primary-50 dark:bg-primary-950/50 text-primary-600 dark:text-primary-400 flex items-center justify-center mb-4 ring-1 ring-primary-500/20 shadow-xs">
      <UIcon
        name="i-lucide-wallet"
        class="w-7 h-7"
      />
    </div>
    <h2 class="text-xl font-bold text-slate-900 dark:text-white tracking-tight">
      Finance
    </h2>
    <p class="mt-1 text-sm text-slate-500 dark:text-slate-400 max-w-sm">
      Main content placeholder. Student tuition, payment plans, invoices, and financial reports will be processed here.
    </p>
  </div>
</template>
