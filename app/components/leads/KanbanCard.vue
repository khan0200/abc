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
    }, 1500)
  } catch (err) {
    console.error('Failed to copy phone', err)
  }
}

const closedReasonLabel = computed(() => {
  switch (props.lead.closedReason) {
    case 'NO_ANSWER':
      return 'No Answer'
    case 'WRONG_NUMBER':
      return 'Wrong #'
    case 'IRRELEVANT':
      return 'Spam'
    default:
      return 'Closed'
  }
})
</script>

<template>
  <div
    :data-id="lead.id"
    :class="[
      'lead-card group relative p-3 rounded-xl border transition-all duration-150 select-none shadow-2xs hover:shadow-md cursor-grab active:cursor-grabbing',
      lead.status === 'COLD'
        ? 'bg-blue-50/90 dark:bg-blue-950/50 border-blue-200/90 dark:border-blue-800/80 hover:border-blue-400 hover:bg-blue-100/70'
        : lead.status === 'WAITING'
          ? 'bg-amber-50/90 dark:bg-amber-950/50 border-amber-200/90 dark:border-amber-800/80 hover:border-amber-400 hover:bg-amber-100/70'
          : 'bg-rose-50/90 dark:bg-rose-950/50 border-rose-200/90 dark:border-rose-800/80 hover:border-rose-400 hover:bg-rose-100/70'
    ]"
  >
    <!-- Row 1: Avatar, Name & Drag Grip -->
    <div class="flex items-center justify-between gap-2">
      <div class="flex items-center gap-2 min-w-0">
        <!-- Compact Initials Badge -->
        <div
          :class="[
            'w-6 h-6 rounded-md flex items-center justify-center font-bold text-[10px] shrink-0',
            lead.status === 'COLD'
              ? 'bg-blue-600 text-white'
              : lead.status === 'WAITING'
                ? 'bg-amber-600 text-white'
                : 'bg-rose-600 text-white'
          ]"
        >
          {{ lead.name.charAt(0).toUpperCase() }}
        </div>

        <h4
          :class="[
            'font-bold text-xs sm:text-sm truncate tracking-tight',
            lead.status === 'COLD'
              ? 'text-blue-950 dark:text-blue-100'
              : lead.status === 'WAITING'
                ? 'text-amber-950 dark:text-amber-100'
                : 'text-rose-950 dark:text-rose-100'
          ]"
        >
          {{ lead.name }}
        </h4>
      </div>

      <!-- Grip icon handle -->
      <div
        :class="[
          'p-0.5 rounded text-slate-400 group-hover:text-slate-700 dark:group-hover:text-slate-200 transition-colors',
          lead.status === 'COLD'
            ? 'text-blue-400 group-hover:text-blue-700'
            : lead.status === 'WAITING'
              ? 'text-amber-400 group-hover:text-amber-700'
              : 'text-rose-400 group-hover:text-rose-700'
        ]"
      >
        <UIcon
          name="i-lucide-grip-vertical"
          class="w-3.5 h-3.5"
        />
      </div>
    </div>

    <!-- Row 2: Phone Number & Course Tag -->
    <div class="flex items-center justify-between gap-2 mt-2 pt-1.5 border-t border-black/5 dark:border-white/10">
      <!-- Phone with Copy -->
      <div class="flex items-center gap-1.5 min-w-0">
        <a
          :href="`tel:${lead.phone}`"
          :class="[
            'inline-flex items-center gap-1 font-mono text-[11px] font-medium transition-colors truncate',
            lead.status === 'COLD'
              ? 'text-blue-900 dark:text-blue-200 hover:text-blue-700'
              : lead.status === 'WAITING'
                ? 'text-amber-950 dark:text-amber-200 hover:text-amber-700'
                : 'text-rose-950 dark:text-rose-200 hover:text-rose-700'
          ]"
          @click.stop
        >
          <UIcon
            name="i-lucide-phone"
            class="w-3 h-3 opacity-60 shrink-0"
          />
          <span class="truncate">{{ lead.phone }}</span>
        </a>

        <button
          type="button"
          class="p-0.5 text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 transition-colors"
          :title="copied ? 'Copied!' : 'Copy phone'"
          @click.stop="copyPhone"
        >
          <UIcon
            :name="copied ? 'i-lucide-check' : 'i-lucide-copy'"
            class="w-3 h-3"
          />
        </button>
      </div>

      <!-- Intended Course Tag / Reason -->
      <div class="flex items-center gap-1 shrink-0">
        <!-- Closed Reason (if Closed) -->
        <span
          v-if="lead.status === 'CLOSED'"
          class="text-[9px] font-bold px-1.5 py-0.5 rounded-md bg-rose-200/90 text-rose-800 dark:bg-rose-900 dark:text-rose-200 border border-rose-300 dark:border-rose-700"
        >
          {{ closedReasonLabel }}
        </span>

        <!-- Course Badge -->
        <span
          :class="[
            'inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-semibold max-w-[120px] truncate shadow-2xs',
            lead.status === 'COLD'
              ? 'bg-blue-100/90 text-blue-800 dark:bg-blue-900/80 dark:text-blue-200 border border-blue-200/80'
              : lead.status === 'WAITING'
                ? 'bg-amber-100/90 text-amber-800 dark:bg-amber-900/80 dark:text-amber-200 border border-amber-200/80'
                : 'bg-rose-100/90 text-rose-800 dark:bg-rose-900/80 dark:text-rose-200 border border-rose-200/80'
          ]"
          :title="lead.courseName"
        >
          <UIcon
            name="i-lucide-book-open"
            class="w-2.5 h-2.5 shrink-0 opacity-70"
          />
          <span class="truncate">{{ lead.courseName }}</span>
        </span>
      </div>
    </div>
  </div>
</template>
