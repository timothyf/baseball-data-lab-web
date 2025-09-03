<template>
  <section class="leaders-view">
    <div class="leaders-content">
      <h1>League Leaders</h1>
      <div class="leader-filters">
        <Dropdown
          v-model="selectedLeague"
          :options="leagueOptions"
          optionLabel="label"
          optionValue="value"
          placeholder="Filter by league"
          showClear
        />
        <Dropdown
          v-model="selectedTeam"
          :options="teamOptions"
          optionLabel="label"
          optionValue="value"
          placeholder="Filter by team"
          showClear
        />
      </div>
      <TabView>
        <TabPanel header="Batting Leaders">
          <DataTable
            v-if="battingLeaders.length"
            :value="battingLeaders"
            class="batting-leaders-table"
            lazy
            :sortField="battingSort.field"
            :sortOrder="battingSort.order"
            @sort="onBattingSort"
          >
            <Column field="rank" header="#"></Column>
            <Column field="playerFullName" header="Player"></Column>
            <Column field="teamAbbrev" header="Team"></Column>
            <Column field="avg" header="AVG" sortable></Column>
            <Column field="doubles" header="2B" sortable></Column>
            <Column field="triples" header="3B" sortable></Column>
            <Column field="homeRuns" header="HR" sortable></Column>
            <Column field="rbi" header="RBI" sortable></Column>
            <Column field="ops" header="OPS" sortable></Column>
            <Column field="stolenBases" header="SB" sortable></Column>
            <Column field="baseOnBalls" header="BB" sortable></Column>
            <Column field="strikeOuts" header="SO" sortable></Column>
          </DataTable>
        </TabPanel>
        <TabPanel header="Pitching Leaders">
          <DataTable
            v-if="pitchingLeaders.length"
            :value="pitchingLeaders"
            class="pitching-leaders-table"
            lazy
            :sortField="pitchingSort.field"
            :sortOrder="pitchingSort.order"
            @sort="onPitchingSort"
          >
            <Column field="rank" header="#"></Column>
            <Column field="playerFullName" header="Player"></Column>
            <Column field="teamAbbrev" header="Team"></Column>
            <Column field="era" header="ERA" sortable></Column>
            <Column field="wins" header="W" sortable></Column>
            <Column field="strikeOuts" header="SO" sortable></Column>
            <Column field="whip" header="WHIP" sortable></Column>
            <Column field="saves" header="SV" sortable></Column>
          </DataTable>
        </TabPanel>
        <TabPanel header="Fielding Leaders">
          <DataTable
            v-if="fieldingLeaders.length"
            :value="fieldingLeaders"
            class="fielding-leaders-table"
            lazy
            :sortField="fieldingSort.field"
            :sortOrder="fieldingSort.order"
            @sort="onFieldingSort"
          >
            <Column field="rank" header="#"></Column>
            <Column field="playerFullName" header="Player"></Column>
            <Column field="teamAbbrev" header="Team"></Column>
            <Column field="fielding" header="FPCT" sortable></Column>
            <Column field="assists" header="A" sortable></Column>
            <Column field="putOuts" header="PO" sortable></Column>
            <Column field="errors" header="E" sortable></Column>
          </DataTable>
        </TabPanel>
      </TabView>
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
import { onMounted, ref, computed, watch } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
import Dialog from 'primevue/dialog';
import 'primevue/dialog/style';
import ProgressSpinner from 'primevue/progressspinner';
import 'primevue/progressspinner/style';
import Dropdown from 'primevue/dropdown';
import 'primevue/dropdown/style';
import teams from '../data/mlbTeams.json';
import {
  fetchBattingLeaders,
  fetchPitchingLeaders,
  fetchFieldingLeaders,
} from '../services/api';
import logger from '../utils/logger';

const battingLeaders = ref([]);
const pitchingLeaders = ref([]);
const fieldingLeaders = ref([]);
const loading = ref(true);

const leagueOptions = [
  { label: 'All Leagues', value: null },
  { label: 'American League', value: 103 },
  { label: 'National League', value: 104 },
];
const selectedLeague = ref(null);
const selectedTeam = ref(null);

const allTeams = [
  ...teams.AL.map((t) => ({ label: t.name, value: t.mlbam_team_id, league: 103 })),
  ...teams.NL.map((t) => ({ label: t.name, value: t.mlbam_team_id, league: 104 })),
];

const teamOptions = computed(() => {
  const opts = [{ label: 'All Teams', value: null }];
  if (!selectedLeague.value) {
    return opts.concat(allTeams);
  }
  return opts.concat(allTeams.filter((t) => t.league === selectedLeague.value));
});

const battingSort = ref({ field: 'homeRuns', order: -1 });
const pitchingSort = ref({ field: 'era', order: 1 });
const fieldingSort = ref({ field: 'fieldingPercentage', order: -1 });

onMounted(async () => {
  loading.value = true;
  try {
    // try {
    //   const res = await fetch('/api/leaders/');
    //   leaders.value = await res.json();
    // } catch (e) {
    //   logger.error('Failed to fetch league leaders:', e);
    //   leaders.value = null;
    // }
    await Promise.all([
      loadBattingLeaders(),
      loadPitchingLeaders(),
      loadFieldingLeaders(),
    ]);
  } catch (e) {
    logger.error('Failed to load leaders data:', e);
  } finally {
    loading.value = false;
  }
});

watch(selectedLeague, () => {
  selectedTeam.value = null;
});

watch([selectedLeague, selectedTeam], async () => {
  loading.value = true;
  try {
    await Promise.all([
      loadBattingLeaders(),
      loadPitchingLeaders(),
      loadFieldingLeaders(),
    ]);
  } finally {
    loading.value = false;
  }
});

async function loadBattingLeaders() {
  const season = new Date().getFullYear();
  const order = battingSort.value.order === 1 ? 'asc' : 'desc';
  const data = await fetchBattingLeaders(
    season,
    selectedLeague.value,
    selectedTeam.value,
    battingSort.value.field,
    order,
    10,
    0,
    {
      useCache: false,     
    },
  );
  battingLeaders.value = Array.isArray(data) ? data : data?.stats || [];
}

async function loadPitchingLeaders() {
  const season = new Date().getFullYear();
  const order = pitchingSort.value.order === 1 ? 'asc' : 'desc';
  const data = await fetchPitchingLeaders(
    season,
    selectedLeague.value,
    selectedTeam.value,
    pitchingSort.value.field,
    order,
    10,
    0,
    {
      useCache: false,
    },
  );
  pitchingLeaders.value = Array.isArray(data) ? data : data?.stats || [];
}

async function loadFieldingLeaders() {
  const season = new Date().getFullYear();
  const order = fieldingSort.value.order === 1 ? 'asc' : 'desc';
  const data = await fetchFieldingLeaders(
    season,
    selectedLeague.value,
    selectedTeam.value,
    fieldingSort.value.field,
    order,
    10,
    0,
    {
      useCache: false,
    },
  );
  fieldingLeaders.value = Array.isArray(data) ? data : data?.stats || [];
}

function onBattingSort(e) {
  battingSort.value = { field: e.sortField, order: e.sortOrder };
  loadBattingLeaders();
}

function onPitchingSort(e) {
  pitchingSort.value = { field: e.sortField, order: e.sortOrder };
  loadPitchingLeaders();
}

function onFieldingSort(e) {
  fieldingSort.value = { field: e.sortField, order: e.sortOrder };
  loadFieldingLeaders();
}
</script>

<style scoped>
.leaders-view {
  display: flex;
  justify-content: center;
  width: 100%;
}

.leaders-content {
  width: 100%;
  max-width: 1100px;
}

.leader-filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.batting-leaders-table,
.pitching-leaders-table,
.fielding-leaders-table {
  width: 100%;
}

.leaders-lists {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
}
</style>
