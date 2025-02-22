<template>
  <RankingTable :columns="columns" :data="data" @row-click="handleRowClick" />
</template>

<script setup>
import RankingTable from '@/components/RankingTable.vue'
import { ref } from 'vue'

const formatter = new Intl.DateTimeFormat('zh-CN', {
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
  hour: '2-digit',
  minute: '2-digit',
  second: '2-digit',
})

const currentTime = ref(formatter.format(new Date()))

const columns = [
  { key: 'rank', label: '排名' },
  { key: 'student_id', label: '学号' },
  { key: 'score', label: '分数' },
  { key: 'submit_time', label: '提交时间' },
]

const data = [
  { rank: 1, student_id: '2021001', score: 100, submit_time: currentTime.value },
  { rank: 2, student_id: '2021002', score: 95, submit_time: currentTime.value },
  { rank: 3, student_id: '2021003', score: 90, submit_time: currentTime.value },
  { rank: 4, student_id: '2021004', score: 85, submit_time: currentTime.value },
  { rank: 5, student_id: '2021005', score: 80, submit_time: currentTime.value },
]

function handleRowClick(row) {
  console.log('Row clicked:', row)
}
</script>
