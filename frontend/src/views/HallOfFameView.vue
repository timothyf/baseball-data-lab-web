<template>
  <section class="hall-of-fame-view">
    <h1>Hall of Fame</h1>
    <table v-if="players.length" class="hof-table">
      <thead>
        <tr>
          <th @click="sortBy('name')">Player</th>
          <th @click="sortBy('first_name')">First Name</th>
          <th @click="sortBy('last_name')">Last Name</th>
          <th @click="sortBy('mlbam_id')">MLBAM ID</th>
          <th @click="sortBy('year')">Year Inducted</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="player in sortedPlayers" :key="player.bbref_id">
          <td>
            <RouterLink
              v-if="player.mlbam_id"
              :to="{ name: 'Player', params: { id: player.mlbam_id }, query: { name: player.name } }"
            >
              {{ player.name || player.bbref_id }}
            </RouterLink>
            <span v-else>{{ player.name || player.bbref_id }}</span>
          </td>
          <td>{{ player.first_name }}</td>
          <td>{{ player.last_name }}</td>
          <td>
            <a
              v-if="player.mlbam_id"
              :href="`https://www.mlb.com/player/${player.mlbam_id}`"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ player.mlbam_id }}
            </a>
          </td>
          <td>{{ player.year }}</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { fetchHallOfFamePlayers } from '../services/api';
import logger from '../utils/logger';

const players = ref([]);
const sortKey = ref('name');
const sortAsc = ref(true);

function sortBy(key) {
  if (sortKey.value === key) {
    sortAsc.value = !sortAsc.value;
  } else {
    sortKey.value = key;
    sortAsc.value = true;
  }
}

const sortedPlayers = computed(() => {
  return [...players.value].sort((a, b) => {
    const valA = a[sortKey.value] ?? '';
    const valB = b[sortKey.value] ?? '';
    if (valA < valB) return sortAsc.value ? -1 : 1;
    if (valA > valB) return sortAsc.value ? 1 : -1;
    return 0;
  });
});

onMounted(async () => {
  try {
    const data = await fetchHallOfFamePlayers();
    players.value = data?.players || [];
  } catch (e) {
    logger.error('Failed to fetch Hall of Fame players:', e);
    players.value = [];
  }
});
</script>

<style scoped>
.hall-of-fame-view {
  padding: 1rem;
}

.hof-table {
  width: 100%;
  border-collapse: collapse;
}

.hof-table th,
.hof-table td {
  padding: 0.5rem;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.hof-table th {
  cursor: pointer;
  background-color: #f5f5f5;
}
</style>

