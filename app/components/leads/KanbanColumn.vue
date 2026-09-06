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
  colorScheme: 'blue' | 'amber' | 'slate'
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
      'flex flex-col h-full rounded-2xl border bg-slate-50/50 dark:bg-slate-950/40 p-3 transition-colors',
      colorScheme === 'blue'
        ? 'border-blue-200/80 dark:border-blue-900/50'
        : colorScheme === 'amber'
          ? 'border-amber-200/80 dark:border-amber-900/50'
          : 'border-slate-200 dark:border-slate-800/80'
    ]"
  >
    <!-- Column Header -->
    <div
      :class="[
        'flex items-center justify-between p-3 rounded-xl border mb-3',
        colorScheme === 'blue'
          ? 'bg-blue-50/80 dark:bg-blue-950/50 border-blue-100 dark:border-blue-900/60'
          : colorScheme === 'amber'
            ? 'bg-amber-50/80 dark:bg-amber-950/50 border-amber-100 dark:border-amber-900/60'
            : 'bg-slate-100/80 dark:bg-slate-900/60 border-slate-200/80 dark:border-slate-800'
      ]"
    >
      <div class="flex items-center gap-2.5">
        <!-- Status color indicator dot -->
        <span
          :class="[
            'w-2.5 h-2.5 rounded-full',
            colorScheme === 'blue'
              ? 'bg-blue-600 dark:bg-blue-400 ring-2 ring-blue-200 dark:ring-blue-900'
              : colorScheme === 'amber'
                ? 'bg-amber-500 dark:bg-amber-400 ring-2 ring-amber-200 dark:ring-amber-900'
                : 'bg-slate-400 dark:bg-slate-500 ring-2 ring-slate-200 dark:ring-slate-800'
          ]"
        />

        <div class="flex flex-col">
          <h3
            :class="[
              'text-sm font-bold tracking-tight',
              colorScheme === 'blue'
                ? 'text-blue-950 dark:text-blue-200'
                : colorScheme === 'amber'
                  ? 'text-amber-950 dark:text-amber-200'
                  : 'text-slate-800 dark:text-slate-200'
            ]"
          >
            {{ title }}
          </h3>
          <span class="text-[11px] text-slate-500 dark:text-slate-400 leading-none">
            {{ subtitle }}
          </span>
        </div>
      </div>

      <!-- Count Badge -->
      <span
        :class="[
          'px-2.5 py-0.5 rounded-full font-bold text-xs shadow-2xs',
          colorScheme === 'blue'
            ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/80 dark:text-blue-300'
            : colorScheme === 'amber'
              ? 'bg-amber-100 text-amber-800 dark:bg-amber-900/80 dark:text-amber-300'
              : 'bg-slate-200 text-slate-700 dark:bg-slate-800 dark:text-slate-300'
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
        class="h-44 rounded-xl border border-dashed border-slate-200 dark:border-slate-800/80 flex flex-col items-center justify-center p-4 text-center text-slate-400 dark:text-slate-600"
      >
        <UIcon name="i-lucide-inbox" class="w-6 h-6 mb-1.5 opacity-60" />
        <span class="text-xs font-medium">No leads in this stage</span>
        <span class="text-[10px] text-slate-400">Drag leads here</span>
      </div>
    </div>
  </div>
</template>
