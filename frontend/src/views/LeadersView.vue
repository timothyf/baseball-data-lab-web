<template>
  <section class="leaders-view">
    <div class="leaders-content">
      <h1>League Leaders</h1>
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
          <div class="leaders-lists">
            <PlayerQuickList
              v-if="leaders?.batting?.HR"
              title="HR Leaders"
              :players="leaders.batting.HR"
            />
            <PlayerQuickList
              v-if="leaders?.batting?.AVG"
              title="AVG Leaders"
              :players="leaders.batting.AVG"
            />
            <PlayerQuickList
              v-if="leaders?.batting?.OPS"
              title="OPS Leaders"
              :players="leaders.batting.OPS"
            />
          </div>
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
          <div class="leaders-lists">
            <PlayerQuickList
              v-if="leaders?.pitching?.ERA"
              title="ERA Leaders"
              :players="leaders.pitching.ERA"
              :decimal-places="2"
            />
            <PlayerQuickList
              v-if="leaders?.pitching?.SO"
              title="SO Leaders"
              :players="leaders.pitching.SO"
            />
            <PlayerQuickList
              v-if="leaders?.pitching?.WHIP"
              title="WHIP Leaders"
              :players="leaders.pitching.WHIP"
              :decimal-places="2"
            />
          </div>
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
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import PlayerQuickList from '../components/PlayerQuickList.vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
import {
  fetchBattingLeaders,
  fetchPitchingLeaders,
  fetchFieldingLeaders,
} from '../services/api';

const leaders = ref(null);
const battingLeaders = ref([]);
const pitchingLeaders = ref([]);
const fieldingLeaders = ref([]);

const battingSort = ref({ field: 'homeRuns', order: -1 });
const pitchingSort = ref({ field: 'era', order: 1 });
const fieldingSort = ref({ field: 'fieldingPercentage', order: -1 });

onMounted(async () => {
  try {
    const res = await fetch('/api/leaders/');
    leaders.value = await res.json();
  } catch (e) {
    console.error('Failed to fetch league leaders:', e);
    leaders.value = null;
  }
  await Promise.all([
    loadBattingLeaders(),
    loadPitchingLeaders(),
    loadFieldingLeaders(),
  ]);
});

async function loadBattingLeaders() {
  const season = new Date().getFullYear();
  const order = battingSort.value.order === 1 ? 'asc' : 'desc';
  const data = await fetchBattingLeaders(
    season,
    battingSort.value.field,
    order,
    10,
    0,
    { useCache: false },
  );
  battingLeaders.value = Array.isArray(data) ? data : data?.stats || [];
}

async function loadPitchingLeaders() {
  const season = new Date().getFullYear();
  const order = pitchingSort.value.order === 1 ? 'asc' : 'desc';
  const data = await fetchPitchingLeaders(
    season,
    pitchingSort.value.field,
    order,
    10,
    0,
    { useCache: false },
  );
  pitchingLeaders.value = Array.isArray(data) ? data : data?.stats || [];
}

async function loadFieldingLeaders() {
  const season = new Date().getFullYear();
  const order = fieldingSort.value.order === 1 ? 'asc' : 'desc';
  const data = await fetchFieldingLeaders(
    season,
    fieldingSort.value.field,
    order,
    10,
    0,
    { useCache: false },
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
  max-width: 1100px;
}

.leaders-lists {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
}
</style>
