<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useSidebar } from '~/composables/useSidebar'

const route = useRoute()
const { isMobileOpen, isCollapsed, navItems, closeMobile, toggleCollapse } = useSidebar()

const expandedItems = ref<Record<string, boolean>>({ settings: true })

const toggleExpand = (id: string) => {
  expandedItems.value[id] = !expandedItems.value[id]
}

const isExpanded = (id: string) => {
  return !!expandedItems.value[id]
}

// Auto-expand if active route belongs to parent
watch(() => route.path, (path) => {
  closeMobile()
  for (const item of navItems) {
    if (item.children && (path === item.to || path.startsWith(`${item.to}/`))) {
      expandedItems.value[item.id] = true
    }
  }
}, { immediate: true })

const isItemActive = (to: string) => {
  if (to === '/') {
    return route.path === '/'
  }
  return route.path === to || route.path.startsWith(`${to}/`)
}
</script>

<template>
  <div>
    <!-- Mobile Backdrop Overlay -->
    <Transition
      enter-active-class="transition-opacity duration-300 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-200 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="isMobileOpen"
        class="fixed inset-0 z-40 bg-slate-900/50 backdrop-blur-xs lg:hidden"
        aria-hidden="true"
        @click="closeMobile"
      />
    </Transition>

    <!-- Sidebar Container -->
    <aside
      id="main-sidebar"
      :class="[
        'fixed inset-y-0 left-0 z-50 flex flex-col bg-white dark:bg-slate-950 border-r border-slate-200 dark:border-slate-800/80 transition-all duration-300 ease-in-out',
        // Desktop width
        isCollapsed ? 'lg:w-20' : 'lg:w-64',
        // Mobile drawer slide-in
        isMobileOpen ? 'translate-x-0 w-72' : '-translate-x-full lg:translate-x-0'
      ]"
      aria-label="Main Navigation"
    >
      <!-- Header / Academy Branding -->
      <div class="h-16 flex items-center justify-between px-4 border-b border-slate-100 dark:border-slate-800/70 shrink-0">
        <NuxtLink
          to="/"
          class="flex items-center gap-3 overflow-hidden group focus:outline-hidden"
          :title="isCollapsed ? 'EduCRM - Education Management' : undefined"
        >
          <!-- Academy Emblem Icon -->
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-600 to-primary-700 flex items-center justify-center text-white shadow-sm shadow-primary-500/20 shrink-0 group-hover:scale-105 transition-transform duration-200">
            <UIcon name="i-lucide-graduation-cap" class="w-6 h-6" />
          </div>

          <!-- Title & Subtitle (hidden when desktop collapsed) -->
          <div
            v-if="!isCollapsed || isMobileOpen"
            class="flex flex-col min-w-0 transition-opacity duration-200"
          >
            <span class="font-bold text-slate-900 dark:text-white tracking-tight leading-tight truncate text-base">
              EduCenter CRM
            </span>
            <span class="text-[11px] font-medium text-slate-400 dark:text-slate-500 uppercase tracking-wider truncate">
              Academy Portal
            </span>
          </div>
        </NuxtLink>

        <!-- Close button for Mobile -->
        <button
          type="button"
          class="lg:hidden p-1.5 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800/60 focus:outline-hidden transition-colors"
          aria-label="Close sidebar"
          @click="closeMobile"
        >
          <UIcon name="i-lucide-x" class="w-5 h-5" />
        </button>

        <!-- Desktop Collapse Button -->
        <button
          type="button"
          class="hidden lg:flex p-1.5 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800/60 focus:outline-hidden transition-colors"
          :title="isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
          @click="toggleCollapse"
        >
          <UIcon
            :name="isCollapsed ? 'i-lucide-panel-left-open' : 'i-lucide-panel-left-close'"
            class="w-4 h-4"
          />
        </button>
      </div>

      <!-- Navigation Menu -->
      <nav class="flex-1 px-3 py-4 overflow-y-auto space-y-1">
        <!-- Section Label (optional, hidden on collapsed) -->
        <div
          v-if="!isCollapsed || isMobileOpen"
          class="px-3 pb-2 text-[11px] font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider"
        >
          Navigation
        </div>

        <!-- Main Menu Items -->
        <div
          v-for="item in navItems"
          :key="item.id"
          class="space-y-1"
        >
          <div class="relative flex items-center">
            <NuxtLink
              :to="item.to"
              :class="[
                'group relative flex-1 flex items-center gap-3 px-3 py-2.5 rounded-xl font-medium text-sm transition-all duration-150 select-none outline-hidden',
                isItemActive(item.to)
                  ? 'bg-primary-50 dark:bg-primary-950/40 text-primary-700 dark:text-primary-300 font-semibold shadow-xs'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-100/80 dark:hover:bg-slate-800/50',
                isCollapsed && !isMobileOpen ? 'justify-center px-0' : ''
              ]"
              :title="isCollapsed && !isMobileOpen ? item.label : undefined"
            >
              <!-- Active Indicator Accent Pill -->
              <span
                v-if="isItemActive(item.to)"
                class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 bg-primary-600 rounded-r-full"
                aria-hidden="true"
              />

              <!-- Icon -->
              <div
                :class="[
                  'flex items-center justify-center shrink-0 w-6 h-6 transition-transform duration-200 group-hover:scale-110',
                  isItemActive(item.to)
                    ? 'text-primary-600 dark:text-primary-400'
                    : 'text-slate-400 dark:text-slate-500 group-hover:text-slate-700 dark:group-hover:text-slate-300'
                ]"
              >
                <UIcon :name="item.icon" class="w-5 h-5" />
              </div>

              <!-- Item Label -->
              <span
                v-if="!isCollapsed || isMobileOpen"
                class="truncate flex-1 tracking-tight"
              >
                {{ item.label }}
              </span>

              <!-- Expand/Collapse Chevron button for submenu -->
              <button
                v-if="item.children && (!isCollapsed || isMobileOpen)"
                type="button"
                class="p-1 rounded-md text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 focus:outline-hidden"
                :aria-expanded="isExpanded(item.id)"
                :title="isExpanded(item.id) ? 'Collapse sub-menu' : 'Expand sub-menu'"
                @click.stop.prevent="toggleExpand(item.id)"
              >
                <UIcon
                  :name="isExpanded(item.id) ? 'i-lucide-chevron-down' : 'i-lucide-chevron-right'"
                  class="w-4 h-4 transition-transform duration-200"
                />
              </button>
            </NuxtLink>
          </div>

          <!-- Nested Submenu for items with children (Settings) -->
          <div
            v-if="item.children && isExpanded(item.id) && (!isCollapsed || isMobileOpen)"
            class="pl-6 pr-1 py-1 space-y-1 ml-4 border-l-2 border-slate-100 dark:border-slate-800/80 transition-all duration-200"
          >
            <NuxtLink
              v-for="child in item.children"
              :key="child.id"
              :to="child.to"
              :class="[
                'group flex items-center gap-2.5 px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all duration-150 outline-hidden',
                route.path === child.to
                  ? 'bg-primary-50/90 dark:bg-primary-950/60 text-primary-700 dark:text-primary-300 font-semibold'
                  : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100/60 dark:hover:bg-slate-800/40'
              ]"
            >
              <UIcon :name="child.icon" class="w-3.5 h-3.5 shrink-0 text-slate-400 group-hover:text-slate-600 dark:group-hover:text-slate-300" />
              <span class="truncate">{{ child.label }}</span>
            </NuxtLink>
          </div>
        </div>
      </nav>

      <!-- Bottom Visual Separation / Status Section -->
      <div class="p-3 border-t border-slate-100 dark:border-slate-800/70 shrink-0">
        <!-- Center / Campus Indicator -->
        <div
          v-if="!isCollapsed || isMobileOpen"
          class="mb-3 px-3 py-2 rounded-lg bg-slate-50 dark:bg-slate-900/60 border border-slate-200/60 dark:border-slate-800/60 flex items-center justify-between text-xs text-slate-500 dark:text-slate-400"
        >
          <div class="flex items-center gap-2 truncate">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span class="font-medium truncate text-slate-700 dark:text-slate-300">Central Campus</span>
          </div>
          <span class="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Active</span>
        </div>

        <!-- User / Admin Profile Snippet -->
        <div
          :class="[
            'flex items-center gap-3 p-2 rounded-xl transition-colors',
            isCollapsed && !isMobileOpen ? 'justify-center p-0' : 'hover:bg-slate-50 dark:hover:bg-slate-900/40'
          ]"
        >
          <div class="w-9 h-9 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-300 flex items-center justify-center font-semibold text-xs shrink-0 ring-2 ring-white dark:ring-slate-900 shadow-xs">
            AD
          </div>

          <div
            v-if="!isCollapsed || isMobileOpen"
            class="flex flex-col min-w-0"
          >
            <span class="text-xs font-semibold text-slate-800 dark:text-slate-200 truncate">
              Sarah Jenkins
            </span>
            <span class="text-[11px] text-slate-400 truncate">
              Director • Central
            </span>
          </div>
        </div>
      </div>
    </aside>
  </div>
</template>
