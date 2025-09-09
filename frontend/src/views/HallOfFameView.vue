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
              <th></th>
              <th>
                <select v-model="yearFilter" data-test="year-filter">
                  <option value="">All</option>
                  <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
                </select>
              </th>
              <th>
                <select v-model="votedByFilter" data-test="voted-by-filter">
                  <option value="">All</option>
                  <option value="BBWAA">BBWAA</option>
                  <option value="Veterans">Veterans</option>
                  <option value="Veterans - Today's Game Era">Veterans - Today's Game Era</option>
                  <option value="Veterans - 1943 and Later">Veterans - 1943 and Later</option>
                  <option value="Classic Baseball Era">Classic Baseball Era</option>
                  <option value="Old Timers">Old Timers</option>
                  <option value="Run Off">Run Off</option>
                  <option value="Negro League">Negro League</option>
                  <option value="Special Election">Special Election</option>
                </select>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="player in paginatedPlayers" :key="player.bbref_id">
              <td>{{ player.first_name }}</td>
              <td>{{ player.last_name }}</td>
              <td>{{ player.position }}</td>
              <td>{{ player.year }}</td>
              <td>{{ player.voted_by }}</td>
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
        <div v-if="hitters.length">
          <h2>Hitters</h2>
          <table class="hof-table">
            <thead>
              <tr>
                <th>Name</th>
                <th v-for="field in hittingFields" :key="field">{{ fieldLabels[field] ?? field }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="h in hitters" :key="h.name">
                <td>{{ h.name }}</td>
                <td v-for="field in hittingFields" :key="field">{{ h[field] ?? '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-if="pitchers.length">
          <h2>Pitchers</h2>
          <table class="hof-table">
            <thead>
              <tr>
                <th>Name</th>
                <th v-for="field in pitchingFields" :key="field">{{ fieldLabels[field] ?? field }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in pitchers" :key="p.name">
                <td>{{ p.name }}</td>
                <td v-for="field in pitchingFields" :key="field">{{ p[field] ?? '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </TabPanel>
    </TabView>
    <LoadingDialog :visible="loading" />
  </section>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { fetchHallOfFamePlayers, fetchPlayerStats } from '../services/api';
import { fieldLabels } from '../config/playerStatsConfig.js';
import logger from '../utils/logger';
import LoadingDialog from '../components/LoadingDialog.vue';
import Paginator from 'primevue/paginator';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';

const players = ref([]);
const hitters = ref([]);
const pitchers = ref([]);
const HOF_CACHE_TTL = 24 * 60 * 60 * 1000;
const sortKey = ref('last_name');
const sortAsc = ref(true);
const loading = ref(true);
const positionFilter = ref('');
const yearFilter = ref('');
const votedByFilter = ref('');
const lastNameSearch = ref('');
const first = ref(0);
const rows = 50;


const hittingFields = ['atBats', 'hits', 'homeRuns', 'rbi', 'avg', 'obp', 'slg', 'ops'];
const pitchingFields = ['wins', 'losses', 'era', 'gamesPitched', 'gamesStarted', 'inningsPitched', 'strikeOuts', 'saves', 'whip'];

watch([sortKey, sortAsc, positionFilter, yearFilter, lastNameSearch, votedByFilter], () => {
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
        (p.last_name ?? '').toLowerCase().includes(lastNameSearch.value.toLowerCase())) &&
      (!votedByFilter.value || p.voted_by === votedByFilter.value)
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

function findGroup(data, name, type) {
  return data?.stats?.find(
    (s) => s.group?.displayName === name && s.type?.displayName === type,
  );
}

async function loadCareerStats() {
  const hit = [];
  const pitch = [];
  for (const p of players.value) {
    if (!p.mlbam_id) continue;
    try {
      const stats = await fetchPlayerStats(p.mlbam_id);
      const name = `${p.first_name ?? ''} ${p.last_name ?? ''}`.trim() || p.name;
      const h = findGroup(stats, 'hitting', 'career')?.splits?.[0]?.stat;
      const pc = findGroup(stats, 'pitching', 'career')?.splits?.[0]?.stat;
      if (h) hit.push({ name, ...h });
      if (pc) pitch.push({ name, ...pc });
    } catch (err) {
      logger.error('Failed to fetch stats for player', p.mlbam_id, err);
    }
  }
  hitters.value = hit.sort((a, b) => collator.compare(a.name, b.name));
  pitchers.value = pitch.sort((a, b) => collator.compare(a.name, b.name));
}

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
    await loadCareerStats();
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

