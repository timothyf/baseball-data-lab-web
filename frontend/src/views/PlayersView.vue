<template>
  <section class="search-page players-view">
    <div class="search-container">
      <h1>Players</h1>
      <SearchAutocomplete
        placeholder="Search for a player"
        optionLabel="name_full"
        searchEndpoint="/api/players/"
        routeName="Player"
      />
    </div>
  </section>
</template>

<script setup>
import SearchAutocomplete from '../components/SearchAutocomplete.vue';
</script>


