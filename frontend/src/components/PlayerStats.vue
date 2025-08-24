<template>
  <div class="player-stats" v-if="stats">
    <div v-if="hittingRows.length">
      <h2>Hitting</h2>
      <table class="stats-table">
        <thead>
          <tr>
            <th>Split</th>
            <th v-for="field in hittingFields" :key="field">{{ field }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in hittingRows" :key="row.label">
            <td>{{ row.label }}</td>
            <td v-for="field in hittingFields" :key="field">{{ row[field] ?? '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="pitchingRows.length">
      <h2>Pitching</h2>
      <table class="stats-table">
        <thead>
          <tr>
            <th>Split</th>
            <th v-for="field in pitchingFields" :key="field">{{ field }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in pitchingRows" :key="row.label">
            <td>{{ row.label }}</td>
            <td v-for="field in pitchingFields" :key="field">{{ row[field] ?? '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';

const { id } = defineProps({ id: String });

const stats = ref(null);

onMounted(async () => {
  try {
    const resp = await fetch(`/api/players/${id}/stats/`);
    if (resp.ok) {
      stats.value = await resp.json();
    }
  } catch (e) {
    console.error('Failed to fetch player stats', e);
  }
});

const hittingFields = ['avg', 'homeRuns', 'rbi'];
const pitchingFields = ['era', 'strikeOuts', 'wins', 'losses'];

function buildRows(seasonStats, careerStats, fields) {
  const rows = [];
  if (seasonStats) {
    for (const teamId of seasonStats.team_ids || []) {
      const team = seasonStats.teams[teamId];
      const row = { label: team.teamName };
      fields.forEach(f => { row[f] = team.stats?.[f]; });
      rows.push(row);
    }
    if (seasonStats.season && Object.keys(seasonStats.season).length) {
      const totalRow = { label: 'Total' };
      fields.forEach(f => { totalRow[f] = seasonStats.season[f]; });
      rows.push(totalRow);
    }
  }
  if (careerStats && careerStats.season && Object.keys(careerStats.season).length) {
    const careerRow = { label: 'Career' };
    fields.forEach(f => { careerRow[f] = careerStats.season[f]; });
    rows.push(careerRow);
  }
  return rows;
}

const hittingRows = computed(() =>
  buildRows(stats.value?.season?.batting, stats.value?.career?.batting, hittingFields)
);
const pitchingRows = computed(() =>
  buildRows(stats.value?.season?.pitching, stats.value?.career?.pitching, pitchingFields)
);
</script>

<style scoped>
.player-stats {
  margin-top: 2rem;
}
.stats-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.5rem;
}
.stats-table th,
.stats-table td {
  padding: 0.5rem;
  border: 1px solid rgba(0,0,0,0.1);
  text-align: center;
}
.stats-table th {
  background: rgba(0,0,0,0.05);
}
</style>

