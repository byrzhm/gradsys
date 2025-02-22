<template>
  <div class="overflow-x-auto">
    <table class="table w-full border border-gray-300 rounded-lg shadow-sm">
      <thead>
        <tr class="bg-gray-100 text-left">
          <th
            v-for="col in columns"
            :key="col.key"
            @click="sortByColumn(col.key)"
            class="p-3 cursor-pointer hover:bg-gray-200 transition-all"
          >
            {{ col.label }}
            <span v-if="sortKey === col.key">{{ sortOrder === 1 ? '▲' : '▼' }}</span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(row, index) in sortedData"
          :key="index"
          @click="emit('row-click', row)"
          class="border-t border-gray-200 hover:bg-gray-100 cursor-pointer transition-all"
        >
          <td v-for="col in columns" :key="col.key" class="p-3">{{ row[col.key] }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  columns: Array,
  data: Array,
})

const emit = defineEmits(['row-click'])

const sortKey = ref(null)
const sortOrder = ref(1) // 1: 升序, -1: 降序

const sortedData = computed(() => {
  if (!sortKey.value) return props.data
  return [...props.data].sort((a, b) => {
    if (a[sortKey.value] < b[sortKey.value]) return -1 * sortOrder.value
    if (a[sortKey.value] > b[sortKey.value]) return 1 * sortOrder.value
    return 0
  })
})

const sortByColumn = (key) => {
  if (sortKey.value === key) {
    sortOrder.value *= -1 // 反转排序
  } else {
    sortKey.value = key
    sortOrder.value = 1
  }
}
</script>
