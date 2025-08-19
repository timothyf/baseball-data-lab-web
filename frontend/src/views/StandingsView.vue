<template>
  <div v-if="standingsStore.standings.length" style="font-family: proxima-nova, 'open Sans', Helvetica, Arial, sans-serif;">
    <div v-for="(record, index) in standingsStore.standings" :key="index" class="division">
      <h3>{{ getDivisionName(record.division?.id)  }}</h3>
      <table class="standings-table">
        <thead>
          <tr>
            <th style="width:180px">Team</th>
            <th>W</th>
            <th>L</th>
            <th>PCT</th>
            <th>GB</th>
            <th>WCGB</th>
            <th>RS</th>
            <th>RA</th>
            <th>rDiff</th>
            <th>xWL</th>
            <th>Home</th>
            <th>Away</th>
            <th>Division</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="teamRecord in record.teamRecords" :key="teamRecord.team.id">
            <td style="font-family: proxima-nova, 'open Sans', Helvetica, Arial, sans-serif; font-weight: normal">{{ teamRecord.team.name }}</td>
            <td>{{ teamRecord.wins }}</td>
            <td>{{ teamRecord.losses }}</td>
            <td>{{ teamRecord.winningPercentage }}</td>
            <td>{{ teamRecord.divisionGamesBack }}</td>
            <td>{{ teamRecord.wildCardGamesBack }}</td>
            <td>{{ teamRecord.runsScored }}</td>
            <td>{{ teamRecord.runsAllowed }}</td>
            <td>{{ teamRecord.runDifferential }}</td>
            <td>{{ teamRecord.records.expectedRecords[0].wins + "-" + teamRecord.records.expectedRecords[0].losses }}</td>
            <td>{{ teamRecord.records.splitRecords[0].wins }} - {{ teamRecord.records.splitRecords[0].losses }}</td>
            <td>{{ teamRecord.records.splitRecords[1].wins +  "-" + teamRecord.records.splitRecords[1].losses }}</td>
            <td>
              {{
              (() => {
                const id = record.division?.id;
                const idx =
                id === 200 || id === 203 ? 0 :
                id === 201 || id === 204 ? 1 : 2;
                const r = teamRecord.records.divisionRecords[idx] || {};
                return `${r.wins}-${r.losses}`;
              })()
              }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <div v-else>
    <p>No standings data available.</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { standingsStore } from '../store/standings';

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

onMounted(() => {
  fetchStandings();
});
</script>

<style scoped>
.standings-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}
.standings-table th,
.standings-table td {
  border: 1px solid #e2e8f0;
  padding: 4px 8px;
  text-align: left;
}
.division {
  margin-bottom: 2rem;
}
</style>
