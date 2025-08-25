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

function buildRows(statData, fields) {
  const splits = statData?.splits || [];
  return splits.map(split => {
    const row = { label: split.season };
    fields.forEach(f => { row[f] = split.stat?.[f]; });
    return row;
  });
}

function findGroup(name) {
  return stats.value?.stats?.find(
    s => s.group?.displayName?.toLowerCase() === name
  );
}

const hittingRows = computed(() =>
  buildRows(findGroup('hitting'), hittingFields)
);
const pitchingRows = computed(() =>
  buildRows(findGroup('pitching'), pitchingFields)
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

