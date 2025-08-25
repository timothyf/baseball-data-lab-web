<template>
  <div class="player-stats" v-if="stats">
    <div v-if="hittingRows.length">
      <h2>Hitting</h2>
      <table class="stats-table">
        <thead>
          <tr>
            <th>Season</th>
            <th v-for="field in hittingFields" :key="field">{{ fieldLabels[field] ?? field }}</th>
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
            <th>Season</th>
            <th v-for="field in pitchingFields" :key="field">{{ fieldLabels[field] ?? field }}</th>
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

const hittingFields = ['team','atBats', 'hits', 'doubles', 'triples', 'avg', 'homeRuns', 'rbi'];
const pitchingFields = ['team','inningsPitched','era', 'strikeOuts', 'wins', 'losses'];

const fieldLabels = {
  atBats: 'AB',
  hits: 'H',
  doubles: '2B',
  triples: '3B',
  avg: 'AVG',
  homeRuns: 'HR',
  rbi: 'RBI',
  inningsPitched: 'IP',
  era: 'ERA',
  strikeOuts: 'SO',
  wins: 'W',
  losses: 'L',
  team: 'Team'
};

function buildRows(statData, fields) {
  const splits = statData?.splits || [];
  return splits.map(split => {
    const row = { label: split.season };
    fields.forEach(f => { row[f] = split.stat?.[f]; });
    row.team = split.team?.id || 'N/A';
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

