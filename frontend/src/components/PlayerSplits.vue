<template>
  <div class="player-splits" v-if="data">
    <div v-if="batting.length">
      <h2>Batting Splits</h2>
      <table class="stats-table">
        <thead>
          <tr>
            <th>Split</th>
            <th v-for="field in battingFields" :key="'bat-'+field">{{ fieldLabels[field] ?? field }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in batting" :key="row.split">
            <td>{{ row.split }}</td>
            <td v-for="field in battingFields" :key="field">{{ row[field] ?? '-' }}</td>
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
            <th v-for="field in pitchingFields" :key="'pit-'+field">{{ fieldLabels[field] ?? field }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in pitching" :key="row.split">
            <td>{{ row.split }}</td>
            <td v-for="field in pitchingFields" :key="field">{{ row[field] ?? '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { fetchPlayerSplits } from '../services/api.js';
import { fieldLabels } from '../config/playerStatsConfig.js';

const { id } = defineProps({ id: String });

const data = ref(null);

onMounted(async () => {
  data.value = await fetchPlayerSplits(id);
});

const batting = computed(() => data.value?.batting || []);
const pitching = computed(() => data.value?.pitching || []);

const battingFields = ['gamesPlayed', 'atBats', 'hits', 'doubles', 'triples', 'homeRuns', 'rbi', 'avg', 'obp', 'slg', 'ops'];
const pitchingFields = ['gamesPlayed', 'gamesPitched', 'inningsPitched', 'strikeOuts', 'baseOnBalls', 'hits', 'homeRuns', 'avg', 'obp', 'slg', 'ops', 'whip'];
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
