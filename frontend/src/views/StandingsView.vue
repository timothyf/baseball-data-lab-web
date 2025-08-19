<template>
  <div v-if="standingsStore.standings.length">
    <div v-for="(record, index) in standingsStore.standings" :key="index" class="division">
      <h2>{{ record.division?.name }}</h2>
      <table class="standings-table">
        <thead>
          <tr>
            <th>Team</th>
            <th>W</th>
            <th>L</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="teamRecord in record.teamRecords" :key="teamRecord.team.id">
            <td>{{ teamRecord.team.name }}</td>
            <td>{{ teamRecord.wins }}</td>
            <td>{{ teamRecord.losses }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <div v-else>
    <p>No standings data available.</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { standingsStore } from '../store/standings';

async function fetchStandings() {
  const resp = await fetch('/api/standings/');
  const data = await resp.json();
  standingsStore.standings = data.records || data;
}

onMounted(() => {
  fetchStandings();
});
</script>

<style scoped>
.standings-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}
.standings-table th,
.standings-table td {
  border: 1px solid #e2e8f0;
  padding: 4px 8px;
  text-align: left;
}
.division {
  margin-bottom: 2rem;
}
</style>
