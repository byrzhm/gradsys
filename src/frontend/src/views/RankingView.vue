<template>
  <RankingTable :columns="columns" :data="data" @row-click="handleRowClick" />
</template>

<script setup>
import RankingTable from '@/components/RankingTable.vue'
import { ref, onMounted } from 'vue'

const columns = [
  { key: 'rank', label: '排名' },
  { key: 'student_id', label: '学号' },
  { key: 'score', label: '分数' },
  { key: 'submit_time', label: '提交时间' },
]

const data = ref([])

const fetchRankingData = async () => {
  try {
    const response = await fetch('/api/v1/ranking');
    const rankingData = await response.json();
    console.log(rankingData); // 或者直接渲染到界面
    data.value = rankingData.items;
  } catch (error) {
    console.error('Error fetching ranking data:', error);
  }
};

onMounted(fetchRankingData);

function handleRowClick(row) {
  console.log('Row clicked:', row)
}
</script>
