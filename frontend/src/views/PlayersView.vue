<template>
  <div>
    <h1>Players</h1>
    <SearchAutocomplete
      placeholder="Search for a player"
      optionLabel="name_full"
      searchEndpoint="/api/players/"
      routeName="Player"
    />
  </div>
</template>

<script setup>
import SearchAutocomplete from '../components/SearchAutocomplete.vue';
</script>

<style scoped>
</style>

