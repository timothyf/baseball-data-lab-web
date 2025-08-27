<template>
  <section class="search-page players-view">
    <div class="content">
      <div class="search-container">
        <h1>Players</h1>
        <SearchAutocomplete
          placeholder="Search for a player"
          optionLabel="name_full"
          searchEndpoint="/api/players/"
          routeName="Player"
          idField="key_mlbam"
        />
      </div>
      <aside class="sidebar">
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
        />
      </aside>
    </div>
  </section>
</template>

<script setup>
import SearchAutocomplete from '../components/SearchAutocomplete.vue';
import PlayerQuickList from '../components/PlayerQuickList.vue';
import { onMounted, ref } from 'vue';

const leaders = ref(null);

onMounted(async () => {
  try {
    const res = await fetch('/api/leaders/');
    leaders.value = await res.json();
  } catch (e) {
    console.error('Failed to fetch league leaders:', e);
    leaders.value = null;
  }
});
</script>

<style scoped>
.players-view {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}
.players-view .content {
  display: flex;
  justify-content: space-around;
  gap: 2rem;
  width: 1100px;
}
.sidebar {
  text-align: left;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  max-width: 600px;
}
.player-list {
  width: 190px;
}
</style>

