<template>
  <section class="hall-of-fame-view">
    <h1>Hall of Fame</h1>
    <table v-if="players.length" class="hof-table">
      <thead>
        <tr>
          <th @click="sortBy('first_name')">First Name</th>
          <th @click="sortBy('last_name')">Last Name</th>
          <th @click="sortBy('mlbam_id')">MLBAM ID</th>
          <th @click="sortBy('year')">Year Inducted</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="player in sortedPlayers" :key="player.bbref_id">
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
const sortKey = ref('last_name');
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

const collator = new Intl.Collator(undefined, { sensitivity: 'base', numeric: true });
const numericKeys = new Set(['year', 'mlbam_id']);

const sortedPlayers = computed(() => {
  const key = sortKey.value;
  const asc = sortAsc.value;
  const isNumeric = numericKeys.has(key);

  return [...players.value].sort((a, b) => {
    const aVal = a[key];
    const bVal = b[key];

    if (isNumeric) {
      const an = Number(aVal);
      const bn = Number(bVal);
      const aBad = Number.isNaN(an);
      const bBad = Number.isNaN(bn);
      if (aBad || bBad) return aBad === bBad ? 0 : aBad ? 1 : -1;
      const cmp = an - bn;
      return asc ? cmp : -cmp;
    }

    const as = (aVal ?? '').toString();
    const bs = (bVal ?? '').toString();
    const aEmpty = !as;
    const bEmpty = !bs;
    if (aEmpty || bEmpty) return aEmpty === bEmpty ? 0 : aEmpty ? 1 : -1;

    const cmp = collator.compare(as, bs);
    return asc ? cmp : -cmp;
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

