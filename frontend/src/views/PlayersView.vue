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
        <PlayerQuickList title="Popular Players" :players="popularPlayers" />
        <PlayerQuickList title="Popular Batters" :players="popularBatters" />
        <PlayerQuickList title="Popular Pitchers" :players="popularPitchers" />
      </aside>
    </div>
  </section>
</template>

<script setup>
import SearchAutocomplete from '../components/SearchAutocomplete.vue';
import PlayerQuickList from '../components/PlayerQuickList.vue';

const popularPlayers = [
  { id: '660271', name: 'Shohei Ohtani' },
  { id: '545361', name: 'Mike Trout' },
  { id: '592450', name: 'Aaron Judge' },
  { id: '605141', name: 'Mookie Betts' },
  { id: '514888', name: 'Jose Altuve' }
];

const popularBatters = [
  { id: '518692', name: 'Freddie Freeman' },
  { id: '665742', name: 'Juan Soto' },
  { id: '547180', name: 'Bryce Harper' },
  { id: '665489', name: 'Vladimir Guerrero Jr.' },
  { id: '646240', name: 'Rafael Devers' }
];

const popularPitchers = [
  { id: '594798', name: 'Jacob deGrom' },
  { id: '453286', name: 'Max Scherzer' },
  { id: '434378', name: 'Justin Verlander' },
  { id: '543037', name: 'Gerrit Cole' },
  { id: '477132', name: 'Clayton Kershaw' }
];
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

