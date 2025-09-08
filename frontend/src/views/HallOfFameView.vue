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
    <LoadingDialog :visible="loading" />
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { fetchHallOfFamePlayers } from '../services/api';
import logger from '../utils/logger';
import LoadingDialog from '../components/LoadingDialog.vue';

const players = ref([]);
const sortKey = ref('name');
const sortAsc = ref(true);
const loading = ref(true);

function sortBy(key) {
  if (sortKey.value === key) {
    sortAsc.value = !sortAsc.value;
  } else {
    sortKey.value = key;
    sortAsc.value = true;
  }
}

const sortedPlayers = computed(() => {
  const collator = new Intl.Collator(undefined, { sensitivity: 'base', numeric: true });
  return [...players.value].sort((a, b) => {
    const key = sortKey.value;
    let valA = a[key];
    let valB = b[key];

    if (key === 'year' || key === 'mlbam_id') {
      // ensure numeric comparison and push invalid values to the end
      valA = Number(valA);
      valB = Number(valB);

      const aInvalid = Number.isNaN(valA);
      const bInvalid = Number.isNaN(valB);
      if (aInvalid && bInvalid) return 0;
      if (aInvalid) return 1;
      if (bInvalid) return -1;

      return sortAsc.value ? valA - valB : valB - valA;
    }

    valA = (valA ?? '').toString();
    valB = (valB ?? '').toString();

    if (!valA && !valB) return 0;
    if (!valA) return 1;
    if (!valB) return -1;

    return sortAsc.value ? collator.compare(valA, valB) : collator.compare(valB, valA);
  });
});

onMounted(async () => {
  try {
    const data = await fetchHallOfFamePlayers();
    players.value = (data?.players || []).map((p) => {
      const mlbam = Number.parseInt(p.mlbam_id, 10);
      const year = Number.parseInt(p.year, 10);
      return {
        ...p,
        mlbam_id: Number.isNaN(mlbam) ? null : mlbam,
        year: Number.isNaN(year) ? null : year,
      };
    });
  } catch (e) {
    logger.error('Failed to fetch Hall of Fame players:', e);
    players.value = [];
  } finally {
    loading.value = false;
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

