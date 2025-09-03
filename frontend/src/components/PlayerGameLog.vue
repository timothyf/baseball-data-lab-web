<template>
  <div v-if="rows.length">
    <table class="stats-table">
      <thead>
        <tr>
          <th>Date</th>
          <th>Opp</th>
          <th v-for="field in fields" :key="field">{{ fieldLabels[field] ?? field }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in rows" :key="row.date">
          <td>{{ row.date }}</td>
          <td>{{ row.opponent }}</td>
          <td v-for="field in fields" :key="field">{{ row[field] ?? '-' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div v-else>
    <p>No game log data available.</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { fetchPlayerGameLog } from '../services/api.js';
import { fieldLabels } from '../config/playerStatsConfig.js';

const props = defineProps({
  id: String,
  statType: { type: String, default: 'hitting' },
  season: { type: Number, default: new Date().getFullYear() },
});

const data = ref(null);

onMounted(async () => {
  data.value = await fetchPlayerGameLog(props.id, props.statType, props.season);
});

const fieldsByType = {
  hitting: ['atBats', 'runs', 'hits', 'homeRuns', 'rbi', 'baseOnBalls', 'strikeOuts', 'avg'],
  pitching: ['inningsPitched', 'runs', 'earnedRuns', 'hits', 'homeRuns', 'baseOnBalls', 'strikeOuts', 'era'],
};

const fields = computed(() => fieldsByType[props.statType] || []);

const rows = computed(() => {
  const splits = data.value?.stats?.[0]?.splits || [];
  return splits.map(s => {
    const stat = s.stat || {};
    const row = {
      date: s.date,
      opponent: s.opponent?.abbreviation,
    };
    fields.value.forEach(f => {
      row[f] = stat[f];
    });
    return row;
  });
});
</script>

<style scoped>
.stats-table {
  margin-top: 1rem;
  border-collapse: collapse;
}
.stats-table th,
.stats-table td {
  border: 1px solid #ddd;
  padding: 0.5rem;
}
.stats-table th {
  background-color: #f5f5f5;
}
</style>
