<template>
  <section class="search-page teams-view">
    <div class="search-container">
      <h1>Teams</h1>
      <SearchAutocomplete
        placeholder="Search for a team"
        optionLabel="full_name"
        searchEndpoint="/api/teams/"
        routeName="Team"
      />
    </div>
  </section>
</template>

<script setup>
import SearchAutocomplete from '../components/SearchAutocomplete.vue';
</script>


