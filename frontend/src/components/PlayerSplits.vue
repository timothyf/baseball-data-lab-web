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
          <tr v-for="split in battingSplitTypes" :key="split">
            <td>{{ splitTypeLabels[split] }}</td>
            <td v-for="field in standardHittingFields" :key="field">
              {{ battingRowsBySplit[split]?.stat?.[field] ?? '-' }}
            </td>
          </tr>
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
          <tr v-for="split in pitchingSplitTypes" :key="split">
            <td>{{ splitTypeLabels[split] }}</td>
            <td v-for="field in standardPitchingFields" :key="field">
              {{ pitchingRowsBySplit[split]?.stat?.[field] ?? '-' }}
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
import {
  standardHittingFields,
  advancedHittingFields,
  standardPitchingFields,
  advancedPitchingFields,
  fieldLabels,
  splitTypeLabels,
  battingSplitTypes,
  pitchingSplitTypes
} from '../config/playerStatsConfig.js';

const { id } = defineProps({ id: String });

const data = ref(null);

onMounted(async () => {
  console.log('Fetching player splits for ID:', id);
  data.value = await fetchPlayerSplits(id);
  console.log('Fetched player splits:', data.value);
});
const batting = computed(() => data.value?.batting || []);
const pitching = computed(() => data.value?.pitching || []);

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
  border: 1px solid #ddd;
  padding: 0.5rem;
}
.stats-table th {
  background-color: rgba(255, 255, 255, 0.1);
}
</style>
