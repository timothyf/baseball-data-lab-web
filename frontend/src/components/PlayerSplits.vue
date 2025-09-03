<template>
  <div class="player-splits" v-if="data">
    <div v-if="batting.length">
      <h2>Batting Splits</h2>
      <table class="stats-table">
        <thead>
          <tr>
            <th>Split</th>
            <th v-for="field in standardHittingFields" :key="field">{{ fieldLabels[field] ?? field }}</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="(group, groupIndex) in splitTypeGroups" :key="groupIndex">
            <tr
              v-for="split in group"
              :key="split"
              :class="{ 'group-separator': groupIndex > 0 && split === group[0] }"
            >
              <td>{{ splitTypeLabels[split] }}</td>
              <td v-for="field in standardHittingFields" :key="field">
                {{ battingRowsBySplit[split]?.stat?.[field] ?? '-' }}
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
    <div v-if="pitching.length">
      <h2>Pitching Splits</h2>
      <table class="stats-table">
        <thead>
          <tr>
            <th>Split</th>
            <th v-for="field in standardPitchingFields" :key="field">{{ fieldLabels[field] ?? field }}</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="(group, groupIndex) in splitTypeGroups" :key="groupIndex">
            <tr
              v-for="split in group"
              :key="split"
              :class="{ 'group-separator': groupIndex > 0 && split === group[0] }"
            >
              <td>{{ splitTypeLabels[split] }}</td>
              <td v-for="field in standardPitchingFields" :key="field">
                {{ pitchingRowsBySplit[split]?.stat?.[field] ?? '-' }}
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
    <div v-if="monthlyBatting.length">
      <h2>Batting Splits by Month</h2>
      <table class="stats-table">
        <thead>
          <tr>
            <th>Month</th>
            <th v-for="field in standardHittingFields" :key="field">{{ fieldLabels[field] ?? field }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in monthlyBatting" :key="row.month">
            <td>{{ formatMonth(row.month) }}</td>
            <td v-for="field in standardHittingFields" :key="field">
              {{ field === 'team' ? row.team?.name ?? '-' : row.stat?.[field] ?? '-' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="monthlyPitching.length">
      <h2>Pitching Splits by Month</h2>
      <table class="stats-table">
        <thead>
          <tr>
            <th>Month</th>
            <th v-for="field in standardPitchingFields" :key="field">{{ fieldLabels[field] ?? field }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in monthlyPitching" :key="row.month">
            <td>{{ formatMonth(row.month) }}</td>
            <td v-for="field in standardPitchingFields" :key="field">
              {{ field === 'team' ? row.team?.name ?? '-' : row.stat?.[field] ?? '-' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { fetchPlayerSplits } from '../services/api.js';
import logger from '../utils/logger';
import {
  standardHittingFields,
  advancedHittingFields,
  standardPitchingFields,
  advancedPitchingFields,
  fieldLabels,
  splitTypeLabels,
  splitTypeGroups
} from '../config/playerStatsConfig.js';

const { id } = defineProps({ id: String });

const data = ref(null);

onMounted(async () => {
  logger.info('Fetching player splits for ID:', id);
  data.value = await fetchPlayerSplits(id);
  logger.info('Fetched player splits:', data.value);
});
const batting = computed(() => data.value?.batting || []);
const pitching = computed(() => data.value?.pitching || []);
const monthlyBatting = computed(() => {
  const splits = data.value?.monthly?.batting || [];
  return [...splits].sort((a, b) => (a.month ?? 0) - (b.month ?? 0));
});
const monthlyPitching = computed(() => {
  const splits = data.value?.monthly?.pitching || [];
  return [...splits].sort((a, b) => (a.month ?? 0) - (b.month ?? 0));
});


const formatMonth = m =>
  new Date(0, (m || 1) - 1).toLocaleString('default', { month: 'long' });

const battingRowsBySplit = computed(() => {
  const map = {};
  batting.value.forEach(r => {
    const code = r.split?.code;
    if (code) map[code] = r;
  });
  return map;
});

const pitchingRowsBySplit = computed(() => {
  const map = {};
  pitching.value.forEach(r => {
    const code = r.split?.code;
    if (code) map[code] = r;
  });
  return map;
});

</script>

<style scoped>
.player-splits {
  margin-top: 2rem;
}
.stats-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 2rem;
}
.stats-table th,
.stats-table td {
  padding: 0.5rem;
  border: 1px solid rgba(0, 0, 0, 0.1);
  text-align: center;
}
.stats-table th {
  background: var(--color-primary);
  color: #fff;
}

.group-separator td {
  border-top: 2px solid #aaa;
}
</style>
