<template>
  <section class="leaders-view">
    <div class="leaders-content">
      <h1>League Leaders</h1>
      <h2>Batting Leaders</h2>
      <DataTable
        v-if="battingLeaders.length"
        :value="battingLeaders"
        class="batting-leaders-table"
        lazy
        :sortField="tableSort.field"
        :sortOrder="tableSort.order"
        @sort="onTableSort"
      >
        <Column field="rank" header="#"></Column>
        <Column field="playerFullName" header="Player"></Column>
        <Column field="teamAbbrev" header="Team"></Column>
        <Column field="avg" header="AVG" sortable></Column>
        <Column field="homeRuns" header="HR" sortable></Column>
        <Column field="rbi" header="RBI" sortable></Column>
        <Column field="doubles" header="2B" sortable></Column>
        <Column field="triples" header="3B" sortable></Column>
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
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import PlayerQuickList from '../components/PlayerQuickList.vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import { fetchBattingLeaders } from '../services/api';

const leaders = ref(null);
const battingLeaders = ref([]);
const tableSort = ref({ field: 'homeRuns', order: -1 });

onMounted(async () => {
  try {
    const res = await fetch('/api/leaders/');
    leaders.value = await res.json();
  } catch (e) {
    console.error('Failed to fetch league leaders:', e);
    leaders.value = null;
  }
  await loadBattingLeaders();
});

async function loadBattingLeaders() {
  const season = new Date().getFullYear();
  const order = tableSort.value.order === 1 ? 'asc' : 'desc';
  const data = await fetchBattingLeaders(
    season,
    tableSort.value.field,
    order,
    10,
    0,
    { useCache: false },
  );
  battingLeaders.value = Array.isArray(data) ? data : data?.stats || [];
}

function onTableSort(e) {
  tableSort.value = { field: e.sortField, order: e.sortOrder };
  loadBattingLeaders();
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
