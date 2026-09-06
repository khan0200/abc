<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import Sortable from 'sortablejs'
import type { Lead, LeadStatus } from '~/types/lead'
import KanbanCard from '~/components/leads/KanbanCard.vue'

const props = defineProps<{
  status: LeadStatus
  title: string
  subtitle: string
  leads: Lead[]
  count: number
  colorScheme: 'blue' | 'amber' | 'red'
}>()

const emit = defineEmits<{
  (e: 'move-lead', id: string, toStatus: LeadStatus): void
}>()

const containerRef = ref<HTMLElement | null>(null)
let sortableInstance: Sortable | null = null

onMounted(() => {
  if (containerRef.value) {
    sortableInstance = new Sortable(containerRef.value, {
      group: 'leads-kanban-board',
      animation: 200,
      ghostClass: 'opacity-30',
      chosenClass: 'ring-2 ring-primary-500 rounded-xl shadow-lg',
      dragClass: 'opacity-90',
      fallbackOnBody: true,
      swapThreshold: 0.65,
      onAdd: (evt) => {
        const id = evt.item.getAttribute('data-id')
        if (id) {
          emit('move-lead', id, props.status)
        }
      }
    })
  }
})

onUnmounted(() => {
  if (sortableInstance) {
    sortableInstance.destroy()
    sortableInstance = null
  }
})
</script>

<template>
  <div
    :class="[
      'flex flex-col h-full rounded-2xl border p-3 transition-colors',
      colorScheme === 'blue'
        ? 'border-blue-300/80 dark:border-blue-900/60 bg-blue-50/40 dark:bg-blue-950/20'
        : colorScheme === 'amber'
          ? 'border-amber-300/80 dark:border-amber-900/60 bg-amber-50/40 dark:bg-amber-950/20'
          : 'border-rose-300/80 dark:border-rose-900/60 bg-rose-50/40 dark:bg-rose-950/20'
    ]"
  >
    <!-- Column Header -->
    <div
      :class="[
        'flex items-center justify-between p-3 rounded-xl border mb-3 shadow-2xs',
        colorScheme === 'blue'
          ? 'bg-blue-50 dark:bg-blue-950/70 border-blue-200 dark:border-blue-900/70'
          : colorScheme === 'amber'
            ? 'bg-amber-50 dark:bg-amber-950/70 border-amber-200 dark:border-amber-900/70'
            : 'bg-rose-50 dark:bg-rose-950/70 border-rose-200 dark:border-rose-900/70'
      ]"
    >
      <div class="flex items-center gap-2.5">
        <!-- Status color indicator dot -->
        <span
          :class="[
            'w-2.5 h-2.5 rounded-full shadow-xs',
            colorScheme === 'blue'
              ? 'bg-blue-600 dark:bg-blue-400 ring-2 ring-blue-200 dark:ring-blue-900'
              : colorScheme === 'amber'
                ? 'bg-amber-500 dark:bg-amber-400 ring-2 ring-amber-200 dark:ring-amber-900'
                : 'bg-rose-600 dark:bg-rose-400 ring-2 ring-rose-200 dark:ring-rose-900'
          ]"
        />

        <div class="flex flex-col">
          <h3
            :class="[
              'text-sm font-bold tracking-tight',
              colorScheme === 'blue'
                ? 'text-blue-950 dark:text-blue-100'
                : colorScheme === 'amber'
                  ? 'text-amber-950 dark:text-amber-100'
                  : 'text-rose-950 dark:text-rose-100'
            ]"
          >
            {{ title }}
          </h3>
          <span
            :class="[
              'text-[11px] leading-none',
              colorScheme === 'blue'
                ? 'text-blue-700/70 dark:text-blue-400/80'
                : colorScheme === 'amber'
                  ? 'text-amber-700/70 dark:text-amber-400/80'
                  : 'text-rose-700/70 dark:text-rose-400/80'
            ]"
          >
            {{ subtitle }}
          </span>
        </div>
      </div>

      <!-- Count Badge -->
      <span
        :class="[
          'px-2.5 py-0.5 rounded-full font-bold text-xs shadow-2xs',
          colorScheme === 'blue'
            ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/90 dark:text-blue-200 border border-blue-200/80 dark:border-blue-800'
            : colorScheme === 'amber'
              ? 'bg-amber-100 text-amber-800 dark:bg-amber-900/90 dark:text-amber-200 border border-amber-200/80 dark:border-amber-800'
              : 'bg-rose-100 text-rose-800 dark:bg-rose-900/90 dark:text-rose-200 border border-rose-200/80 dark:border-rose-800'
        ]"
      >
        {{ count }}
      </span>
    </div>

    <!-- Cards Droppable Container -->
    <div
      ref="containerRef"
      :data-status="status"
      class="flex-1 overflow-y-auto space-y-2.5 min-h-[350px] pb-6 rounded-xl"
    >
      <KanbanCard
        v-for="lead in leads"
        :key="lead.id"
        :lead="lead"
      />

      <!-- Empty State -->
      <div
        v-if="leads.length === 0"
        :class="[
          'h-44 rounded-xl border border-dashed flex flex-col items-center justify-center p-4 text-center',
          colorScheme === 'blue'
            ? 'border-blue-200 dark:border-blue-900/50 text-blue-400'
            : colorScheme === 'amber'
              ? 'border-amber-200 dark:border-amber-900/50 text-amber-400'
              : 'border-rose-200 dark:border-rose-900/50 text-rose-400'
        ]"
      >
        <UIcon name="i-lucide-inbox" class="w-6 h-6 mb-1.5 opacity-60" />
        <span class="text-xs font-medium">No leads in this stage</span>
        <span class="text-[10px] opacity-70">Drag leads here</span>
      </div>
    </div>
  </div>
</template>
