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

<style scoped>
.search-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  color: #fff;
  padding: 2rem 1rem;
}

.search-container {
  max-width: 600px;
  width: 100%;
  text-align: center;
}

.search-container h1 {
  font-size: 2rem;
  margin: 0 0 1rem;
  font-weight: 600;
}

.search-container :deep(.p-autocomplete),
.search-container :deep(.p-autocomplete input) {
  width: 100%;
}
</style>

