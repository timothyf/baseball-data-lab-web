<template>
  <section class="standings">
    <div class="standings-container">
      <div v-if="standingsStore.standings.length">
        <TabView>
          <TabPanel header="Standard">
            <nav class="division-links">
              <div class="league-row">
                <a
                  v-for="record in standingsStore.standingsByLeague.al"
                  :key="record.division?.id"
                  :href="`#standard-division-${record.division?.id}`"
                >
                  {{ getDivisionName(record.division?.id) }}
                </a>
              </div>
              <div class="league-row">
                <a
                  v-for="record in standingsStore.standingsByLeague.nl"
                  :key="record.division?.id"
                  :href="`#standard-division-${record.division?.id}`"
                >
                  {{ getDivisionName(record.division?.id) }}
                </a>
              </div>
            </nav>
            <div
              v-for="record in standingsStore.standings"
              :key="record.division?.id"
              class="division-card"
              :id="`standard-division-${record.division?.id}`"
            >
              <h3>{{ getDivisionName(record.division?.id) }}</h3>
              <DataTable class="standings-table" :value="record.teamRecords" responsiveLayout="scroll">
                <Column header="Team" style="width:180px">
                  <template #body="{ data }">
                    <RouterLink
                      :to="{
                        name: 'Team',
                        params: { mlbam_team_id: data.team.id },
                        query: { name: data.team.name }
                      }"
                    >
                      {{ data.team.name }}
                    </RouterLink>
                  </template>
                </Column>
                <Column field="wins" header="W"></Column>
                <Column field="losses" header="L"></Column>
                <Column field="winningPercentage" header="PCT"></Column>
                <Column field="divisionGamesBack" header="GB"></Column>
                <Column
                  field="wildCardGamesBack"
                  header="WCGB"
                  style="border-right: 1px solid #ccc"
                ></Column>
                <Column header="L10">
                  <template #body="{ data }">
                    {{ lastTenRecord(data) }}
                  </template>
                </Column>
                <Column header="STRK" style="border-right: 1px solid #ccc">
                  <template #body="{ data }">
                    {{ data.streak?.streakCode }}
                  </template>
                </Column>
                <Column field="runsScored" header="RS"></Column>
                <Column field="runsAllowed" header="RA"></Column>
                <Column field="runDifferential" header="rDiff">
                  <template #body="{ data }">
                    {{ formatRunDifferential(data.runDifferential) }}
                  </template>
                </Column>
                <Column header="X-W/L" style="border-right: 1px solid #ccc">
                  <template #body="{ data }">
                    {{ `${data.records.expectedRecords[0].wins}-${data.records.expectedRecords[0].losses}` }}
                  </template>
                </Column>
                <Column header="HOME">
                  <template #body="{ data }">
                    {{ homeRecord(data) }}
                  </template>
                </Column>
                <Column header="AWAY">
                  <template #body="{ data }">
                    {{ awayRecord(data) }}
                  </template>
                </Column>              
              </DataTable>
            </div>
          </TabPanel>

          <TabPanel header="Expanded">  
            <nav class="division-links">
              <div class="league-row">
                <a
                  v-for="record in standingsStore.standingsByLeague.al"
                  :key="record.division?.id"
                  :href="`#expanded-division-${record.division?.id}`"
                >
                  {{ getDivisionName(record.division?.id) }}
                </a>
              </div>
              <div class="league-row">
                <a
                  v-for="record in standingsStore.standingsByLeague.nl"
                  :key="record.division?.id"
                  :href="`#expanded-division-${record.division?.id}`"
                >
                  {{ getDivisionName(record.division?.id) }}
                </a>
              </div>
            </nav>
            <div
              v-for="record in standingsStore.standings"
              :key="record.division?.id"
              class="division-card"
              :id="`expanded-division-${record.division?.id}`"
            >
              <h3>{{ getDivisionName(record.division?.id) }}</h3>
              <DataTable class="standings-table" :value="record.teamRecords" responsiveLayout="scroll">
                <Column header="Team" style="width:180px">
                  <template #body="{ data }">
                    <RouterLink
                      :to="{
                        name: 'Team',
                        params: { mlbam_team_id: data.team.id },
                        query: { name: data.team.name }
                      }"
                    >
                      {{ data.team.name }}
                    </RouterLink>
                  </template>
                </Column>
                <Column field="wins" header="W"></Column>
                <Column field="losses" header="L"></Column>
                <Column field="winningPercentage" header="PCT"></Column>
                <Column field="divisionGamesBack" header="GB"></Column>
                <Column
                  field="wildCardGamesBack"
                  header="WCGB"
                  style="border-right: 1px solid #ccc"
                ></Column>
                <Column header="XTRA">
                  <template #body="{ data }">
                    {{ extraInningRecord(data) }}
                  </template>
                </Column>
                <Column header="1 RUN" style="border-right: 1px solid #ccc">
                  <template #body="{ data }">
                    {{ oneRunRecord(data) }}
                  </template>
                </Column>
                <Column header="DAY">
                  <template #body="{ data }">
                    {{ dayRecord(data) }}
                  </template>
                </Column>
                <Column header="NIGHT">
                  <template #body="{ data }">
                    {{ nightRecord(data) }}
                  </template>
                </Column>
                <Column header="GRASS">
                  <template #body="{ data }">
                    {{ grassRecord(data) }}
                  </template>
                </Column>
                <Column header="TURF" style="border-right: 1px solid #ccc">
                  <template #body="{ data }">
                    {{ turfRecord(data) }}
                  </template>
                </Column>
                <Column header="EAST">
                  <template #body="{ data }">
                    {{ divisionRecord(data, 201) }}
                  </template>
                </Column>
                <Column header="CENTRAL">
                  <template #body="{ data }">
                    {{ divisionRecord(data, 202) }}
                  </template>
                </Column>
                <Column header="WEST">
                  <template #body="{ data }">
                    {{ divisionRecord(data, 203) }}
                  </template>
                </Column>
                <Column header="AL/NL" style="border-right: 1px solid #ccc">
                  <template #body="{ data }">
                    {{ leagueRecord(data) }}
                  </template>
                </Column>
                <Column header="vs R">
                  <template #body="{ data }">
                    {{ splitRecord(data, 'right') }}
                  </template>
                </Column>
                <Column header="vs L">
                  <template #body="{ data }">
                    {{ splitRecord(data, 'left') }}
                  </template>
                </Column>
              </DataTable>
            </div>
          </TabPanel>
        </TabView>
      </div>
    </div>
    <Dialog
      v-model:visible="loading"
      modal
      :closable="false"
      :draggable="false"
      :dismissableMask="false"
      :closeOnEscape="false"
      class="loading-dialog"
    >
      <div class="loading-content">
        <ProgressSpinner />
        <p>Loading data...</p>
      </div>
    </Dialog>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useStandingsStore } from '../store/standings';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
import Dialog from 'primevue/dialog';
import 'primevue/dialog/style';
import ProgressSpinner from 'primevue/progressspinner';
import 'primevue/progressspinner/style';

const standingsStore = useStandingsStore();
const loading = ref(true);

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

function leagueRecord(teamRecord) {
  const divisionId = String(teamRecord.division?.id);
  const isAL = ['200','201','202'].includes(divisionId);
  // MLB Stats API league ids: 103 = AL, 104 = NL
  const oppositeLeagueId = isAL ? 103 : 104;
  const lr = (teamRecord.records?.leagueRecords || [])
    .find(r => r.league?.id === oppositeLeagueId);
  if (lr) return `${lr.wins}-${lr.losses}`;
  return '';
}

function splitRecord(teamRecord, type) {
  const split = teamRecord.records?.splitRecords?.find(r => r.type === type);
  return split ? `${split.wins}-${split.losses}` : '';
}

const lastTenRecord      = (tr) => splitRecord(tr, 'lastTen');
const homeRecord         = (tr) => splitRecord(tr, 'home');
const awayRecord         = (tr) => splitRecord(tr, 'away');
const extraInningRecord  = (tr) => splitRecord(tr, 'extraInning');
const oneRunRecord       = (tr) => splitRecord(tr, 'oneRun');
const nightRecord        = (tr) => splitRecord(tr, 'night');
const dayRecord          = (tr) => splitRecord(tr, 'day');
const grassRecord        = (tr) => splitRecord(tr, 'grass');
const turfRecord         = (tr) => splitRecord(tr, 'turf');

function formatRunDifferential(diff) {
  return diff > 0 ? `+${diff}` : diff;
}

onMounted(async () => {
  try {
    await standingsStore.ensureStandings();
  } finally {
    loading.value = false;
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
  max-width: 1440px;
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

:deep(.standings-table .p-datatable-header),
:deep(.standings-table .p-datatable-thead > tr > th) {
  background-color: var(--color-accent);
  color: var(--color-primary);
  text-align: center;
}

:deep(.p-datatable-column-header-content) {
  text-align: center;
  display: inline;
}

:deep(.standings-table .p-datatable-tbody > tr > td) {
  font-size: 13px;
  font-family: proxima-nova, "open Sans", Helvetica, Arial, sans-serif;
  text-align: center;
}

/* Left-align team column header and cells */
:deep(.standings-table .p-datatable-thead > tr > th:first-child),
:deep(.standings-table .p-datatable-thead > tr > th:first-child .p-datatable-column-header-content) {
  text-align: left;
}

:deep(.standings-table .p-datatable-tbody > tr > td:first-child) {
  text-align: left !important;
  justify-content: flex-start;
}

:deep(.standings-table .p-datatable-tbody > tr > td a) {
  font-weight: bold;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
}

</style>
