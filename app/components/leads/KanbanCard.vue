<script setup lang="ts">
import { computed, ref } from 'vue'
import type { Lead } from '~/types/lead'

const props = defineProps<{
  lead: Lead
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
      'lead-card group relative p-4 rounded-xl border transition-all duration-200 select-none shadow-xs hover:shadow-md cursor-grab active:cursor-grabbing',
      lead.status === 'COLD'
        ? 'bg-blue-50/85 dark:bg-blue-950/40 border-blue-200/90 dark:border-blue-800/80 hover:border-blue-400 hover:bg-blue-100/70 dark:hover:bg-blue-900/50'
        : lead.status === 'WAITING'
          ? 'bg-amber-50/85 dark:bg-amber-950/40 border-amber-200/90 dark:border-amber-800/80 hover:border-amber-400 hover:bg-amber-100/70 dark:hover:bg-amber-900/50'
          : 'bg-rose-50/85 dark:bg-rose-950/40 border-rose-200/90 dark:border-rose-800/80 hover:border-rose-400 hover:bg-rose-100/70 dark:hover:bg-rose-900/50'
    ]"
  >
    <!-- Top Row: Lead Name & Drag Handle -->
    <div class="flex items-start justify-between gap-2 mb-2">
      <div class="flex items-center gap-2.5 min-w-0">
        <!-- Initials Avatar -->
        <div
          :class="[
            'w-8 h-8 rounded-lg flex items-center justify-center font-bold text-xs shrink-0 shadow-2xs',
            lead.status === 'COLD'
              ? 'bg-blue-600 text-white dark:bg-blue-500 ring-2 ring-blue-200 dark:ring-blue-900'
              : lead.status === 'WAITING'
                ? 'bg-amber-600 text-white dark:bg-amber-500 ring-2 ring-amber-200 dark:ring-amber-900'
                : 'bg-rose-600 text-white dark:bg-rose-500 ring-2 ring-rose-200 dark:ring-rose-900'
          ]"
        >
          {{ lead.name.charAt(0).toUpperCase() }}
        </div>

        <div class="min-w-0">
          <h4
            :class="[
              'font-bold text-sm truncate tracking-tight',
              lead.status === 'COLD'
                ? 'text-blue-950 dark:text-blue-100'
                : lead.status === 'WAITING'
                  ? 'text-amber-950 dark:text-amber-100'
                  : 'text-rose-950 dark:text-rose-100'
            ]"
          >
            {{ lead.name }}
          </h4>
          <span
            :class="[
              'text-[11px] block truncate font-medium',
              lead.status === 'COLD'
                ? 'text-blue-600/70 dark:text-blue-400/80'
                : lead.status === 'WAITING'
                  ? 'text-amber-700/70 dark:text-amber-400/80'
                  : 'text-rose-700/70 dark:text-rose-400/80'
            ]"
          >
            {{ formatRelativeTime(lead.createdAt) }}
          </span>
        </div>
      </div>

      <!-- Drag handle indicator -->
      <div
        :class="[
          'p-1 rounded-md transition-colors',
          lead.status === 'COLD'
            ? 'text-blue-400 hover:text-blue-700 dark:text-blue-500 dark:hover:text-blue-300'
            : lead.status === 'WAITING'
              ? 'text-amber-400 hover:text-amber-700 dark:text-amber-500 dark:hover:text-amber-300'
              : 'text-rose-400 hover:text-rose-700 dark:text-rose-500 dark:hover:text-rose-300'
        ]"
      >
        <UIcon name="i-lucide-grip-vertical" class="w-4 h-4" />
      </div>
    </div>

    <!-- Phone Number Row with Quick Copy -->
    <div
      :class="[
        'flex items-center justify-between gap-2 mt-2.5 pt-2 border-t text-xs',
        lead.status === 'COLD'
          ? 'border-blue-200/60 dark:border-blue-800/50'
          : lead.status === 'WAITING'
            ? 'border-amber-200/60 dark:border-amber-800/50'
            : 'border-rose-200/60 dark:border-rose-800/50'
      ]"
    >
      <a
        :href="`tel:${lead.phone}`"
        :class="[
          'inline-flex items-center gap-1.5 font-mono text-[11px] font-medium transition-colors',
          lead.status === 'COLD'
            ? 'text-blue-900 dark:text-blue-200 hover:text-blue-700'
            : lead.status === 'WAITING'
              ? 'text-amber-950 dark:text-amber-200 hover:text-amber-700'
              : 'text-rose-950 dark:text-rose-200 hover:text-rose-700'
        ]"
        @click.stop
      >
        <UIcon name="i-lucide-phone" class="w-3.5 h-3.5 opacity-70" />
        <span>{{ lead.phone }}</span>
      </a>

      <button
        type="button"
        :class="[
          'p-1 rounded-md transition-colors',
          lead.status === 'COLD'
            ? 'text-blue-400 hover:text-blue-700 hover:bg-blue-200/50 dark:hover:bg-blue-900/60'
            : lead.status === 'WAITING'
              ? 'text-amber-400 hover:text-amber-700 hover:bg-amber-200/50 dark:hover:bg-amber-900/60'
              : 'text-rose-400 hover:text-rose-700 hover:bg-rose-200/50 dark:hover:bg-rose-900/60'
        ]"
        :title="copied ? 'Copied!' : 'Copy phone number'"
        @click.stop="copyPhone"
      >
        <UIcon :name="copied ? 'i-lucide-check' : 'i-lucide-copy'" class="w-3.5 h-3.5" />
      </button>
    </div>

    <!-- Course Badge & Source -->
    <div
      :class="[
        'flex flex-wrap items-center justify-between gap-1.5 mt-3 pt-2 border-t',
        lead.status === 'COLD'
          ? 'border-blue-200/60 dark:border-blue-800/50'
          : lead.status === 'WAITING'
            ? 'border-amber-200/60 dark:border-amber-800/50'
            : 'border-rose-200/60 dark:border-rose-800/50'
      ]"
    >
      <!-- Intended Course Badge -->
      <div
        :class="[
          'inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-semibold max-w-[170px] truncate shadow-2xs',
          lead.status === 'COLD'
            ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/80 dark:text-blue-200 border border-blue-200/80 dark:border-blue-700/60'
            : lead.status === 'WAITING'
              ? 'bg-amber-100 text-amber-800 dark:bg-amber-900/80 dark:text-amber-200 border border-amber-200/80 dark:border-amber-700/60'
              : 'bg-rose-100 text-rose-800 dark:bg-rose-900/80 dark:text-rose-200 border border-rose-200/80 dark:border-rose-700/60'
        ]"
      >
        <UIcon name="i-lucide-book-open" class="w-3 h-3 shrink-0 opacity-80" />
        <span class="truncate">{{ lead.courseName }}</span>
      </div>

      <!-- Closed Reason Badge (if Closed) -->
      <span
        v-if="lead.status === 'CLOSED'"
        class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-rose-200/80 text-rose-800 dark:bg-rose-900 dark:text-rose-200 border border-rose-300 dark:border-rose-700"
      >
        {{ closedReasonLabel }}
      </span>

      <!-- Source Badge (if active) -->
      <span
        v-else-if="lead.source"
        :class="[
          'text-[10px] font-medium tracking-tight',
          lead.status === 'COLD'
            ? 'text-blue-600/70 dark:text-blue-400/80'
            : 'text-amber-700/70 dark:text-amber-400/80'
        ]"
      >
        {{ lead.source }}
      </span>
    </div>

    <!-- Optional Notes Snippet if present -->
    <p
      v-if="lead.notes"
      :class="[
        'mt-2 text-[11px] line-clamp-1 italic',
        lead.status === 'COLD'
          ? 'text-blue-700/60 dark:text-blue-400/60'
          : lead.status === 'WAITING'
            ? 'text-amber-800/60 dark:text-amber-400/60'
            : 'text-rose-800/60 dark:text-rose-400/60'
      ]"
    >
      "{{ lead.notes }}"
    </p>
  </div>
</template>
