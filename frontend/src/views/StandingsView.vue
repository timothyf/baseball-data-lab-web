<template>
  <section class="standings">
    <div class="standings-container">
      <div v-if="standingsStore.standings.length">
        <nav class="division-links">
          <div class="league-row">
            <a
              v-for="(record, index) in americanLeagueDivisions"
              :key="`al-link-${index}`"
              :href="`#division-${record.division?.id}`"
            >
              {{ getDivisionName(record.division?.id) }}
            </a>
          </div>
          <div class="league-row">
            <a
              v-for="(record, index) in nationalLeagueDivisions"
              :key="`nl-link-${index}`"
              :href="`#division-${record.division?.id}`"
            >
              {{ getDivisionName(record.division?.id) }}
            </a>
          </div>
        </nav>
        <div
          v-for="(record, index) in standingsStore.standings"
          :key="index"
          class="division-card"
          :id="`division-${record.division?.id}`"
        >
          <h3>{{ getDivisionName(record.division?.id)  }}</h3>
          <DataTable class="standings-table" :value="record.teamRecords" responsiveLayout="scroll">
            <Column field="team.name" header="Team" style="width:180px"></Column>
            <Column field="wins" header="W"></Column>
            <Column field="losses" header="L"></Column>
            <Column field="winningPercentage" header="PCT"></Column>
            <Column field="divisionGamesBack" header="GB"></Column>
            <Column field="wildCardGamesBack" header="WCGB"></Column>
            <Column field="runsScored" header="RS"></Column>
            <Column field="runsAllowed" header="RA"></Column>
            <Column field="runDifferential" header="rDiff">
              <template #body="{ data }">
                {{ formatRunDifferential(data.runDifferential) }}
              </template>
            </Column>
            <Column header="xWL">
              <template #body="{ data }">
                {{ `${data.records.expectedRecords[0].wins}-${data.records.expectedRecords[0].losses}` }}
              </template>
            </Column>
            <Column header="Home">
              <template #body="{ data }">
                {{ `${data.records.splitRecords[0].wins} - ${data.records.splitRecords[0].losses}` }}
              </template>
            </Column>
            <Column header="Away">
              <template #body="{ data }">
                {{ `${data.records.splitRecords[1].wins}-${data.records.splitRecords[1].losses}` }}
              </template>
            </Column>
            <Column header="Division">
              <template #body="{ data }">
                {{ divisionRecord(data, record.division?.id) }}
              </template>
            </Column>
          </DataTable>
        </div>
      </div>
      <div v-else>
        <p>Standings data is loading.</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useStandingsStore } from '../store/standings';

const standingsStore = useStandingsStore();

// Cache standings by season to avoid refetching on remount
const standingsCache = new Map();

const americanLeagueDivisions = computed(() =>
  standingsStore.standings.filter((record) =>
    ['200', '201', '202'].includes(String(record.division?.id))
  )
);

const nationalLeagueDivisions = computed(() =>
  standingsStore.standings.filter((record) =>
    ['203', '204', '205'].includes(String(record.division?.id))
  )
);

async function fetchStandings(season) {
  const resp = await fetch('/api/standings/');
  const data = await resp.json();
  standingsStore.standings = data.records || data;
  standingsCache.set(season, standingsStore.standings);
}

function getDivisionName(divisionId) {
  const divisionNames = {
    '200': 'American League West',
    '201': 'American League East',
    '202': 'American League Central',
    '203': 'National League West',
    '204': 'National League East',
    '205': 'National League Central'
  };
  return divisionNames[divisionId] || divisionId;
}

function divisionRecord(teamRecord, divisionId) {
  const idx =
    divisionId === 200 || divisionId === 203 ? 0 :
    divisionId === 201 || divisionId === 204 ? 1 : 2;
  const r = teamRecord.records.divisionRecords[idx] || {};
  return `${r.wins}-${r.losses}`;
}

function formatRunDifferential(diff) {
  return diff > 0 ? `+${diff}` : diff;
}

onMounted(() => {
  const season = new Date().getFullYear();
  if (!standingsStore.standings.length) {
    if (standingsCache.has(season)) {
      standingsStore.standings = standingsCache.get(season);
    } else {
      fetchStandings(season);
    }
  } else if (!standingsCache.has(season)) {
    standingsCache.set(season, standingsStore.standings);
  }
});
</script>

<style scoped>
.standings {
  font-family: var(--font-base);
  min-height: 100vh;
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  color: #fff;
  padding: 2rem 1rem;
  scroll-behavior: smooth;
}

.standings-container {
  max-width: 1000px;
  margin: 0 auto;
}

.division-links {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.league-row {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.league-row a {
  color: var(--color-accent);
  text-decoration: underline;
}
.division-card {
  background: rgba(255, 255, 255, 0.15);
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 2rem;
}

.division-card h3 {
  margin-top: 0;
  text-align: center;
  color: var(--color-accent);
}

.standings-table .p-datatable-header,
.standings-table .p-datatable-thead > tr > th {
  background-color: var(--color-accent);
  color: var(--color-primary);
}
</style>
