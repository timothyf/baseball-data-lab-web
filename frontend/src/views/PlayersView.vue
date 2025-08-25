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
          v-if="leaders?.pitching?.ERA"
          title="ERA Leaders"
          :players="leaders.pitching.ERA"
        />
        <PlayerQuickList
          v-if="leaders?.pitching?.SO"
          title="SO Leaders"
          :players="leaders.pitching.SO"
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
  align-items: flex-start;
}
.players-view .content {
  display: flex;
  align-items: flex-start;
  gap: 2rem;
}
.sidebar {
  text-align: left;
}
</style>

