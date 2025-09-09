<template>
  <section class="hall-of-fame-view">
    <h1>Hall of Fame</h1>
    <TabView>
      <TabPanel header="Inductees">
        <table v-if="players.length" class="hof-table">
          <thead>
            <tr>
              <th @click="sortBy('first_name')">First Name</th>
              <th @click="sortBy('last_name')">Last Name</th>
              <th @click="sortBy('position')">Position</th>
              <th @click="sortBy('year')">Year Inducted</th>
              <th @click="sortBy('voted_by')">Voted By</th>
              <th @click="sortBy('mlbam_id')">MLBAM ID</th>
            </tr>
            <tr class="filters">
              <th></th>
              <th>
                <input
                  v-model="lastNameSearch"
                  type="text"
                  placeholder="Search"
                  data-test="last-name-search"
                />
              </th>
              <th>
                <select v-model="positionFilter" data-test="position-filter">
                  <option value="">All</option>
                  <option v-for="pos in positions" :key="pos" :value="pos">
                    {{ pos }}
                  </option>
                </select>
              </th>
              <th>
                <select v-model="yearFilter" data-test="year-filter">
                  <option value="">All</option>
                  <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
                </select>
              </th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="player in paginatedPlayers" :key="player.bbref_id">
              <td>{{ player.first_name }}</td>
              <td>{{ player.last_name }}</td>
              <td>{{ player.position }}</td>
              <td>{{ player.year }}</td>
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
              <td>{{ player.voted_by }}</td>
            </tr>
          </tbody>
        </table>
        <Paginator
          v-if="sortedPlayers.length > rows"
          :first="first"
          :rows="rows"
          :totalRecords="sortedPlayers.length"
          @page="onPage"
        />
      </TabPanel>
      <TabPanel header="Career Stats">
        <!-- Career Stats content coming soon -->
      </TabPanel>
    </TabView>
    <LoadingDialog :visible="loading" />
  </section>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { fetchHallOfFamePlayers } from '../services/api';
import logger from '../utils/logger';
import LoadingDialog from '../components/LoadingDialog.vue';
import Paginator from 'primevue/paginator';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';

const players = ref([]);
const HOF_CACHE_TTL = 24 * 60 * 60 * 1000;
const sortKey = ref('last_name');
const sortAsc = ref(true);
const loading = ref(true);
const positionFilter = ref('');
const yearFilter = ref('');
const lastNameSearch = ref('');
const first = ref(0);
const rows = 50;

watch([sortKey, sortAsc, positionFilter, yearFilter, lastNameSearch], () => {
  first.value = 0;
});

function sortBy(key) {
  if (sortKey.value === key) {
    sortAsc.value = !sortAsc.value;
  } else {
    sortKey.value = key;
    sortAsc.value = true;
  }
}

function onPage(event) {
  first.value = event.first;
}

const collator = new Intl.Collator(undefined, { sensitivity: 'base', numeric: true });
const numericKeys = new Set(['year', 'mlbam_id']);

const positions = computed(() => {
  const set = new Set();
  for (const p of players.value) {
    if (p.position) set.add(p.position);
  }
  return [...set].sort((a, b) => collator.compare(a, b));
});

const years = computed(() => {
  const set = new Set();
  for (const p of players.value) {
    if (p.year != null) set.add(p.year);
  }
  return [...set].sort((a, b) => a - b);
});

const filteredPlayers = computed(() =>
  players.value.filter(
    (p) =>
      (!positionFilter.value || p.position === positionFilter.value) &&
      (!yearFilter.value || p.year === Number(yearFilter.value)) &&
      (!lastNameSearch.value ||
        (p.last_name ?? '').toLowerCase().includes(lastNameSearch.value.toLowerCase()))
  )
);

const sortedPlayers = computed(() => {
  const key = sortKey.value;
  const asc = sortAsc.value;
  const isNumeric = numericKeys.has(key);
  const data = filteredPlayers.value;

  return [...data].sort((a, b) => {
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

const paginatedPlayers = computed(() => {
  const start = first.value;
  return sortedPlayers.value.slice(start, start + rows);
});

onMounted(async () => {
  try {
    const data = await fetchHallOfFamePlayers({ persistTTL: HOF_CACHE_TTL });
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

.filters th {
  cursor: default;
}

.filters select {
  width: 100%;
}

.filters input {
  width: 100%;
}
</style>

