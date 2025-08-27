<template>
  <div class="player-stats" v-if="stats">
    <div v-if="standardHittingRows.length">
      <h2>Standard Hitting</h2>
      <table class="stats-table">
        <thead>
          <tr>
            <th>Season</th>
            <th v-for="field in standardHittingFields" :key="field">{{ fieldLabels[field] ?? field }}</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="row in standardHittingRows"
            :key="row.label"
            :class="{ 'career-total': row.label === 'Career' }"
          >
            <td>{{ row.label }}</td>
            <td v-for="field in standardHittingFields" :key="field">{{ row[field] ?? '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="advancedHittingRows.length">
      <h2>Advanced Hitting</h2>
      <table class="stats-table">
        <thead>
          <tr>
            <th>Season</th>
            <th v-for="field in advancedHittingFields" :key="field">{{ fieldLabels[field] ?? field }}</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="row in advancedHittingRows"
            :key="row.label"
            :class="{ 'career-total': row.label === 'Career' }"
          >
            <td>{{ row.label }}</td>
            <td v-for="field in advancedHittingFields" :key="field">{{ row[field] ?? '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="standardPitchingRows.length">
      <h2>Standard Pitching</h2>
      <table class="stats-table">
        <thead>
          <tr>
            <th>Season</th>
            <th v-for="field in standardPitchingFields" :key="field">{{ fieldLabels[field] ?? field }}</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="row in standardPitchingRows"
            :key="row.label"
            :class="{ 'career-total': row.label === 'Career' }"
          >
            <td>{{ row.label }}</td>
            <td v-for="field in standardPitchingFields" :key="field">{{ row[field] ?? '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="advancedPitchingRows.length">
      <h2>Advanced Pitching</h2>
      <table class="stats-table">
        <thead>
          <tr>
            <th>Season</th>
            <th v-for="field in advancedPitchingFields" :key="field">{{ fieldLabels[field] ?? field }}</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="row in advancedPitchingRows"
            :key="row.label"
            :class="{ 'career-total': row.label === 'Career' }"
          >
            <td>{{ row.label }}</td>
            <td v-for="field in advancedPitchingFields" :key="field">{{ row[field] ?? '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import {
  standardHittingFields,
  advancedHittingFields,
  standardPitchingFields,
  advancedPitchingFields,
  fieldLabels
} from '../config/playerStatsConfig.js';


const { id } = defineProps({ id: String });

const stats = ref(null);
const teamAbbrevs = ref({});

onMounted(async () => {
  try {
    const resp = await fetch(`/api/players/${id}/stats/`);
    if (resp.ok) {
      stats.value = await resp.json();
      await fetchTeamAbbrevs(stats.value?.stats);
    }
  } catch (e) {
    console.error('Failed to fetch player stats', e);
  }
});



async function fetchTeamAbbrevs(statGroups) {
  const ids = new Set();
  statGroups?.forEach(group => {
    group?.splits?.forEach(split => {
      const tid = split.team?.id;
      if (tid) ids.add(tid);
    });
  });
  await Promise.all(
    Array.from(ids).map(async tid => {
      if (teamAbbrevs.value[tid]) return;
      try {
        const resp = await fetch(`/api/teams/${tid}/`);
        if (resp.ok) {
          const data = await resp.json();
          teamAbbrevs.value[tid] = data.abbrev || tid;
        }
      } catch (e) {
        console.error('Failed to fetch team info', e);
      }
    })
  );
}

function buildRows(statData, fields, defaultLabel) {
  const splits = statData?.splits || [];
  return splits.map(split => {
    const row = { label: split.season || defaultLabel };
    fields.forEach(f => { row[f] = split.stat?.[f]; });
    const teamId = split.team?.id;
    row.team = teamAbbrevs.value[teamId] || (teamId ?? 'Total');
    return row;
  });
}

function findGroup(name, statType) {
  return stats.value?.stats?.find(
    s => s.group?.displayName === name && s.type?.displayName === statType
  );
}

const standardHittingRows = computed(() => {
  const year = buildRows(findGroup('hitting', 'yearByYear'), standardHittingFields);
  const career = buildRows(findGroup('hitting', 'career'), standardHittingFields, 'Career');
  return [...year, ...career];
});

const advancedHittingRows = computed(() => {
  const year = buildRows(
    findGroup('hitting', 'yearByYearAdvanced'),
    advancedHittingFields
  );
  const career = buildRows(
    findGroup('hitting', 'careerAdvanced'),
    advancedHittingFields,
    'Career'
  );
  return [...year, ...career];
});

const standardPitchingRows = computed(() => {
  const year = buildRows(
    findGroup('pitching', 'yearByYear'),
    standardPitchingFields
  );
  const career = buildRows(
    findGroup('pitching', 'career'),
    standardPitchingFields,
    'Career'
  );
  return [...year, ...career];
});

const advancedPitchingRows = computed(() => {
  const year = buildRows(
    findGroup('pitching', 'yearByYearAdvanced'),
    advancedPitchingFields
  );
  const career = buildRows(
    findGroup('pitching', 'careerAdvanced'),
    advancedPitchingFields,
    'Career'
  );
  return [...year, ...career];
});

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
  background: var(--color-primary);
  color: #fff;
}
.stats-table tr.career-total {
  background: #e6f7ff;
}
</style>

