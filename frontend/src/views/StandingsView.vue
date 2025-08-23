<template>
  <section class="standings">
    <div class="standings-container">
      <div v-if="standingsStore.standings.length">
        <div v-for="(record, index) in standingsStore.standings" :key="index" class="division">
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
            <Column field="runDifferential" header="rDiff"></Column>
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
import { onMounted } from 'vue';
import { useStandingsStore } from '../store/standings';

const standingsStore = useStandingsStore();

async function fetchStandings() {
  const resp = await fetch('/api/standings/');
  const data = await resp.json();
  standingsStore.standings = data.records || data;
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

onMounted(() => {
  fetchStandings();
});
</script>

<style scoped>
.standings {
  font-family: var(--font-base);
  min-height: 100vh;
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  color: #fff;
  padding: 2rem 1rem;
}

.standings-container {
  max-width: 1000px;
  margin: 0 auto;
}

.division {
  margin-bottom: 2rem;
}

.standings-table .p-datatable-header,
.standings-table .p-datatable-thead > tr > th {
  background-color: var(--color-accent);
  color: var(--color-primary);
}
</style>
