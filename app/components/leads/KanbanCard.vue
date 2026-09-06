<script setup lang="ts">
import type { Lead } from '~/types/lead'

const props = defineProps<{
  lead: Lead
}>()

const emit = defineEmits<{
  (e: 'update-reason', id: string, reason: string): void
}>()

const copied = ref(false)

const copyPhone = async () => {
  try {
    await navigator.clipboard.writeText(props.lead.phone)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy phone', err)
  }
}

const formatRelativeTime = (isoString: string) => {
  try {
    const date = new Date(isoString)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / (1000 * 60))
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins}m ago`
    if (diffHours < 24) return `${diffHours}h ago`
    if (diffDays === 1) return 'Yesterday'
    return `${diffDays}d ago`
  } catch {
    return 'Recent'
  }
}

const closedReasonLabel = computed(() => {
  switch (props.lead.closedReason) {
    case 'NO_ANSWER':
      return 'No Answer'
    case 'WRONG_NUMBER':
      return 'Wrong Number'
    case 'IRRELEVANT':
      return 'Irrelevant / Spam'
    default:
      return 'Closed'
  }
})
</script>

<template>
  <div
    :data-id="lead.id"
    :class="[
      'lead-card group relative p-4 rounded-xl border transition-all duration-200 select-none bg-white dark:bg-slate-900 shadow-2xs hover:shadow-md cursor-grab active:cursor-grabbing',
      lead.status === 'COLD'
        ? 'border-blue-100 dark:border-blue-900/60 hover:border-blue-300 dark:hover:border-blue-700'
        : lead.status === 'WAITING'
          ? 'border-amber-100 dark:border-amber-900/60 hover:border-amber-300 dark:hover:border-amber-700'
          : 'border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 opacity-95'
    ]"
  >
    <!-- Top Row: Lead Name & Drag Handle -->
    <div class="flex items-start justify-between gap-2 mb-2">
      <div class="flex items-center gap-2.5 min-w-0">
        <!-- Initials Avatar -->
        <div
          :class="[
            'w-8 h-8 rounded-lg flex items-center justify-center font-bold text-xs shrink-0',
            lead.status === 'COLD'
              ? 'bg-blue-50 text-blue-700 dark:bg-blue-950 dark:text-blue-300 ring-1 ring-blue-500/20'
              : lead.status === 'WAITING'
                ? 'bg-amber-50 text-amber-700 dark:bg-amber-950 dark:text-amber-300 ring-1 ring-amber-500/20'
                : 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300'
          ]"
        >
          {{ lead.name.charAt(0).toUpperCase() }}
        </div>

        <div class="min-w-0">
          <h4 class="font-bold text-sm text-slate-900 dark:text-white truncate tracking-tight">
            {{ lead.name }}
          </h4>
          <span class="text-[11px] text-slate-400 dark:text-slate-500 block truncate">
            {{ formatRelativeTime(lead.createdAt) }}
          </span>
        </div>
      </div>

      <!-- Drag handle indicator -->
      <div class="p-1 rounded-md text-slate-300 dark:text-slate-600 group-hover:text-slate-500 dark:group-hover:text-slate-400 transition-colors">
        <UIcon name="i-lucide-grip-vertical" class="w-4 h-4" />
      </div>
    </div>

    <!-- Phone Number Row with Quick Copy -->
    <div class="flex items-center justify-between gap-2 mt-2.5 pt-2 border-t border-slate-100 dark:border-slate-800/80 text-xs">
      <a
        :href="`tel:${lead.phone}`"
        class="inline-flex items-center gap-1.5 text-slate-600 dark:text-slate-300 hover:text-primary-600 dark:hover:text-primary-400 font-mono text-[11px] font-medium"
        @click.stop
      >
        <UIcon name="i-lucide-phone" class="w-3.5 h-3.5 text-slate-400" />
        <span>{{ lead.phone }}</span>
      </a>

      <button
        type="button"
        class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-1 rounded-md hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
        :title="copied ? 'Copied!' : 'Copy phone number'"
        @click.stop="copyPhone"
      >
        <UIcon :name="copied ? 'i-lucide-check' : 'i-lucide-copy'" class="w-3.5 h-3.5" />
      </button>
    </div>

    <!-- Course Badge & Source -->
    <div class="flex flex-wrap items-center justify-between gap-1.5 mt-3 pt-2 border-t border-slate-100 dark:border-slate-800/80">
      <!-- Intended Course Badge -->
      <div class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-semibold bg-slate-100 dark:bg-slate-800/90 text-slate-700 dark:text-slate-200 max-w-[170px] truncate">
        <UIcon name="i-lucide-book-open" class="w-3 h-3 text-primary-600 dark:text-primary-400 shrink-0" />
        <span class="truncate">{{ lead.courseName }}</span>
      </div>

      <!-- Closed Reason Badge (if Closed) -->
      <span
        v-if="lead.status === 'CLOSED'"
        class="text-[10px] font-medium px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400 border border-slate-200 dark:border-slate-700"
      >
        {{ closedReasonLabel }}
      </span>

      <!-- Source or Manager Badge (if active) -->
      <span
        v-else-if="lead.source"
        class="text-[10px] text-slate-400 dark:text-slate-500 font-medium tracking-tight"
      >
        {{ lead.source }}
      </span>
    </div>

    <!-- Optional Notes Snippet if present -->
    <p
      v-if="lead.notes"
      class="mt-2 text-[11px] text-slate-400 dark:text-slate-500 line-clamp-1 italic"
    >
      "{{ lead.notes }}"
    </p>
  </div>
</template>
