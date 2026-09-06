<script setup lang="ts">
import { ref } from 'vue'
import { useLeads } from '~/composables/useLeads'
import { useCourses } from '~/composables/useCourses'
import type { LeadStatus, ClosedReason } from '~/types/lead'
import KanbanColumn from '~/components/leads/KanbanColumn.vue'
import AddLeadModal from '~/components/leads/AddLeadModal.vue'

useSeoMeta({
  title: 'Leads • Kanban Pipeline • Education Center CRM',
  description: 'Manage prospective student inquiries through a visual drag-and-drop Kanban pipeline.'
})

const {
  searchQuery,
  selectedCourseId,
  coldLeads,
  waitingLeads,
  closedLeads,
  counts,
  updateLeadStatus,
  reorderLead
} = useLeads()

const { courses } = useCourses()

const isAddModalOpen = ref(false)

// Reason selection when moving to Closed
const pendingClosedLeadId = ref<string | null>(null)
const pendingNewIndex = ref<number>(0)
const isReasonModalOpen = ref(false)
const selectedReason = ref<ClosedReason>('NO_ANSWER')

const handleMoveLead = (payload: { id: string; fromStatus: LeadStatus; toStatus: LeadStatus; newIndex: number }) => {
  const { id, toStatus, newIndex } = payload
  if (toStatus === 'CLOSED') {
    pendingClosedLeadId.value = id
    pendingNewIndex.value = newIndex
    isReasonModalOpen.value = true
  } else {
    reorderLead(id, toStatus, newIndex)
  }
}

const confirmClosedReason = () => {
  if (pendingClosedLeadId.value) {
    reorderLead(pendingClosedLeadId.value, 'CLOSED', pendingNewIndex.value, selectedReason.value)
    pendingClosedLeadId.value = null
    isReasonModalOpen.value = false
  }
}

const cancelClosedReason = () => {
  if (pendingClosedLeadId.value) {
    // Default to NO_ANSWER if dismissed
    reorderLead(pendingClosedLeadId.value, 'CLOSED', pendingNewIndex.value, 'NO_ANSWER')
    pendingClosedLeadId.value = null
    isReasonModalOpen.value = false
  }
}
</script>

<template>
  <div class="h-full flex flex-col space-y-5">
    <!-- Top Bar: Title, Search, Filter & Prominent + Add Lead Button -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-2 border-b border-slate-200/80 dark:border-slate-800/80">
      <div>
        <div class="flex items-center gap-3">
          <h1 class="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">
            Leads
          </h1>
          <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-primary-50 text-primary-700 dark:bg-primary-950/60 dark:text-primary-300 border border-primary-200 dark:border-primary-900">
            {{ counts.total }} total
          </span>
        </div>
        <p class="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-0.5">
          Drag and drop prospective student cards between stages to update their progress.
        </p>
      </div>

      <!-- Controls & Add Button -->
      <div class="flex flex-wrap items-center gap-2.5">
        <!-- Search Input -->
        <div class="relative w-full sm:w-60">
          <UIcon
            name="i-lucide-search"
            class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2"
          />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search name, phone..."
            class="w-full pl-9 pr-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-xs text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 transition-all shadow-2xs"
          />
          <button
            v-if="searchQuery"
            type="button"
            class="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
            @click="searchQuery = ''"
          >
            <UIcon name="i-lucide-x" class="w-3.5 h-3.5" />
          </button>
        </div>

        <!-- Course Filter (Dynamic from Settings) -->
        <div class="w-full sm:w-44">
          <select
            v-model="selectedCourseId"
            class="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-xs text-slate-700 dark:text-slate-300 focus:outline-hidden focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 shadow-2xs truncate"
          >
            <option value="all">All Courses</option>
            <option v-for="course in courses" :key="course.id" :value="course.id">
              {{ course.name }}
            </option>
          </select>
        </div>

        <!-- Prominent + Add Lead Button -->
        <button
          type="button"
          class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-primary-600 hover:bg-primary-700 active:scale-[0.98] text-white text-xs font-bold shadow-sm shadow-primary-600/30 transition-all focus:outline-hidden cursor-pointer"
          @click="isAddModalOpen = true"
        >
          <UIcon name="i-lucide-plus" class="w-4 h-4" />
          <span>Add Lead</span>
        </button>
      </div>
    </div>

    <!-- Main Kanban Board Area (3 Columns: Cold, Waiting, Closed/Invalid) -->
    <div class="flex-1 grid grid-cols-1 md:grid-cols-3 gap-4 lg:gap-6 min-h-[550px]">
      <!-- Column 1: Cold -->
      <KanbanColumn
        status="COLD"
        title="Cold"
        subtitle="New Inquiries & Contacts"
        :leads="coldLeads"
        :count="counts.COLD"
        color-scheme="blue"
        @move-lead="handleMoveLead"
      />

      <!-- Column 2: Waiting -->
      <KanbanColumn
        status="WAITING"
        title="Waiting"
        subtitle="Communicated & Ready"
        :leads="waitingLeads"
        :count="counts.WAITING"
        color-scheme="amber"
        @move-lead="handleMoveLead"
      />

      <!-- Column 3: Closed / Invalid -->
      <KanbanColumn
        status="CLOSED"
        title="Closed / Invalid"
        subtitle="No Answer, Wrong #, Dead"
        :leads="closedLeads"
        :count="counts.CLOSED"
        color-scheme="red"
        @move-lead="handleMoveLead"
      />
    </div>

    <!-- Add Lead Modal -->
    <AddLeadModal
      v-model="isAddModalOpen"
    />

    <!-- Reason Selection Modal for Closed / Invalid -->
    <Teleport to="body">
      <Transition
        enter-active-class="transition-opacity duration-200 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-opacity duration-150 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="isReasonModalOpen"
          class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-xs"
        >
          <div class="w-full max-w-sm rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 shadow-xl space-y-4">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 flex items-center justify-center">
                <UIcon name="i-lucide-archive" class="w-5 h-5" />
              </div>
              <div>
                <h4 class="text-sm font-bold text-slate-900 dark:text-white">
                  Specify Closed Reason
                </h4>
                <p class="text-xs text-slate-500">
                  Categorize why this lead is closing.
                </p>
              </div>
            </div>

            <div class="space-y-2">
              <label class="flex items-center gap-3 p-3 rounded-xl border border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800/60 cursor-pointer">
                <input
                  v-model="selectedReason"
                  type="radio"
                  value="NO_ANSWER"
                  class="text-primary-600 focus:ring-primary-500"
                />
                <div class="text-xs">
                  <span class="font-semibold text-slate-800 dark:text-slate-200 block">No Answer</span>
                  <span class="text-slate-400">Repeatedly unreached by phone/chat</span>
                </div>
              </label>

              <label class="flex items-center gap-3 p-3 rounded-xl border border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800/60 cursor-pointer">
                <input
                  v-model="selectedReason"
                  type="radio"
                  value="WRONG_NUMBER"
                  class="text-primary-600 focus:ring-primary-500"
                />
                <div class="text-xs">
                  <span class="font-semibold text-slate-800 dark:text-slate-200 block">Wrong Number</span>
                  <span class="text-slate-400">Invalid phone or wrong person answered</span>
                </div>
              </label>

              <label class="flex items-center gap-3 p-3 rounded-xl border border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800/60 cursor-pointer">
                <input
                  v-model="selectedReason"
                  type="radio"
                  value="IRRELEVANT"
                  class="text-primary-600 focus:ring-primary-500"
                />
                <div class="text-xs">
                  <span class="font-semibold text-slate-800 dark:text-slate-200 block">Irrelevant / Spam</span>
                  <span class="text-slate-400">Junk inquiry or marketing message</span>
                </div>
              </label>
            </div>

            <div class="flex items-center justify-end gap-2 pt-2">
              <button
                type="button"
                class="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800"
                @click="cancelClosedReason"
              >
                Skip / Default
              </button>
              <button
                type="button"
                class="px-4 py-1.5 rounded-lg bg-primary-600 text-white text-xs font-bold hover:bg-primary-700"
                @click="confirmClosedReason"
              >
                Confirm Reason
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>
