<script setup lang="ts">
const settingsCards = [
  {
    title: 'Staff Management',
    description: 'Create and manage system user accounts, assign platform roles (Director, Branch Director, Teacher, Manager).',
    to: '/settings/staff',
    icon: 'i-lucide-user-cog',
    fields: ['User full name', 'Platform role assignment', 'Login credentials']
  },
  {
    title: 'Courses',
    description: 'Setup educational courses, curriculum levels, and standard tuition prices.',
    to: '/settings/courses',
    icon: 'i-lucide-book-open',
    fields: ['Course name', 'Difficulty / Grade level', 'Tuition price']
  },
  {
    title: 'Payment Settings',
    description: 'Configure collection receivers, payment methods, and receipt quick-pick notes.',
    to: '/settings/payments',
    icon: 'i-lucide-credit-card',
    fields: ['Payment method (Cash, Card, Transfer)', 'Designated receiver', 'Quick pick notes']
  }
]
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
    <NuxtLink
      v-for="card in settingsCards"
      :key="card.to"
      :to="card.to"
      class="group p-6 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 hover:border-primary-500/50 hover:shadow-md transition-all flex flex-col justify-between"
    >
      <div>
        <div class="w-12 h-12 rounded-xl bg-primary-50 dark:bg-primary-950/50 text-primary-600 dark:text-primary-400 flex items-center justify-center mb-4 ring-1 ring-primary-500/20 group-hover:scale-105 transition-transform">
          <UIcon :name="card.icon" class="w-6 h-6" />
        </div>
        <h3 class="text-base font-bold text-slate-900 dark:text-white tracking-tight">
          {{ card.title }}
        </h3>
        <p class="mt-1 text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
          {{ card.description }}
        </p>

        <ul class="mt-4 space-y-1.5 border-t border-slate-100 dark:border-slate-800/80 pt-3">
          <li
            v-for="field in card.fields"
            :key="field"
            class="flex items-center gap-2 text-xs text-slate-600 dark:text-slate-400"
          >
            <UIcon name="i-lucide-check-circle-2" class="w-3.5 h-3.5 text-primary-600 dark:text-primary-400 shrink-0" />
            <span>{{ field }}</span>
          </li>
        </ul>
      </div>

      <div class="mt-6 flex items-center gap-1.5 text-xs font-semibold text-primary-600 dark:text-primary-400 group-hover:translate-x-1 transition-transform">
        <span>Configure section</span>
        <UIcon name="i-lucide-arrow-right" class="w-4 h-4" />
      </div>
    </NuxtLink>
  </div>
</template>
