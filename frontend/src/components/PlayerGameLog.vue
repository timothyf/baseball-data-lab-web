<template>
  <div v-if="groupedRows.length">
    <table class="stats-table">
      <thead>
        <tr>
          <th>Date</th>
          <th>Opp</th>
          <th v-for="field in fields" :key="field">{{ fieldLabels[field] ?? field }}</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="group in groupedRows" :key="group.month">
          <tr class="month-row">
            <td :colspan="2 + fields.length">{{ group.month }}</td>
          </tr>
          <tr
            v-for="row in group.games"
            :key="row.date"
            @click="row.gamePk && navigateToGame(row.gamePk)"
            class="log-row"
          >
            <td>
              <RouterLink
                v-if="row.gamePk"
                :to="{ name: 'Game', params: { game_pk: row.gamePk } }"
                @click.stop
              >
                {{ row.date }}
              </RouterLink>
              <span v-else>{{ row.date }}</span>
            </td>
            <td>{{ row.opponent }}</td>
            <td v-for="field in fields" :key="field">{{ row[field] ?? '-' }}</td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
  <div v-else>
    <p>No game log data available.</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { fetchPlayerGameLog } from '../services/api.js';
import { fieldLabels } from '../config/playerStatsConfig.js';

const props = defineProps({
  id: String,
  statType: { type: String, default: 'hitting' },
  season: { type: Number, default: new Date().getFullYear() },
});

const data = ref(null);
const router = useRouter();

onMounted(async () => {
  data.value = await fetchPlayerGameLog(props.id, props.statType, props.season);
});

const fieldsByType = {
  hitting: ['atBats', 'runs', 'hits', 'homeRuns', 'rbi', 'baseOnBalls', 'strikeOuts', 'avg'],
  pitching: ['inningsPitched', 'runs', 'earnedRuns', 'hits', 'homeRuns', 'baseOnBalls', 'strikeOuts', 'era'],
};

const fields = computed(() => fieldsByType[props.statType] || []);

const groupedRows = computed(() => {
  const splits = data.value?.stats?.[0]?.splits || [];
  const groups = [];
  let currentMonth = '';
  let currentGroup = null;
  splits.forEach(s => {
    const stat = s.stat || {};
    const dateObj = new Date(s.date);
    const month = dateObj.toLocaleString('default', { month: 'long', year: 'numeric' });
    if (month !== currentMonth) {
      currentGroup = { month, games: [] };
      groups.push(currentGroup);
      currentMonth = month;
    }
    const row = {
      date: s.date,
      opponent: s.opponent?.abbreviation,
      gamePk: s.game?.gamePk,
    };
    fields.value.forEach(f => {
      row[f] = stat[f];
    });
    currentGroup.games.push(row);
  });
  return groups;
});

const navigateToGame = (pk) => {
  router.push({ name: 'Game', params: { game_pk: pk } });
};
</script>

<style scoped>
.stats-table {
  margin-top: 1rem;
}

.month-row td {
  background-color: #eaeaea;
  font-weight: bold;
}

.log-row {
  cursor: pointer;
}
</style>
