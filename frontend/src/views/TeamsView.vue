<template>
  <div>
    <h1>Teams</h1>
    <SearchAutocomplete
      placeholder="Search for a team"
      optionLabel="full_name"
      searchEndpoint="/api/teams/"
      routeName="Team"
    />
  </div>
</template>

<script setup>
import SearchAutocomplete from '../components/SearchAutocomplete.vue';
</script>

<style scoped>
</style>

