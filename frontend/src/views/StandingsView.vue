<template>
  <div v-if="standingsStore.standings.length" style="font-family: proxima-nova, 'open Sans', Helvetica, Arial, sans-serif;">
    <div v-for="(record, index) in standingsStore.standings" :key="index" class="division">
      <h3>{{ getDivisionName(record.division?.id)  }}</h3>
      <DataTable :value="record.teamRecords">
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
</template>

<script setup>
import { onMounted } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import 'primevue/datatable/style';
import 'primevue/column/style';
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
.division {
  margin-bottom: 2rem;
}
</style>
