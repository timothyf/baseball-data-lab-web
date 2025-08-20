<template>
  <div>
    <h1>Players</h1>
    <AutoComplete
      v-model="selectedPlayer"
      :suggestions="suggestions"
      @complete="searchPlayers"
      optionLabel="name_full"
      placeholder="Search for a player"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import AutoComplete from 'primevue/autocomplete';
import 'primevue/autocomplete/style';

const selectedPlayer = ref(null);
const suggestions = ref([]);

async function searchPlayers(event) {
  const query = event.query;
  if (!query) {
    suggestions.value = [];
    return;
  }
  try {
    const resp = await fetch(`/api/players/?q=${encodeURIComponent(query)}`);
    if (resp.ok) {
      suggestions.value = await resp.json();
    } else {
      suggestions.value = [];
    }
  } catch (err) {
    suggestions.value = [];
  }
}
</script>

<style scoped>
</style>
