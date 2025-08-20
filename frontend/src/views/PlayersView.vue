<template>
  <div>
    <h1>Players</h1>
    <AutoComplete
      v-model="selectedPlayer"
      :suggestions="suggestions"
      @complete="searchPlayers"
      @item-select="onSelect"
      optionLabel="name_full"
      placeholder="Search for a player"
    >
      <template #option="{ option }">
        <div>{{ option.name_full }}</div>
      </template>
    </AutoComplete>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import AutoComplete from 'primevue/autocomplete';
import 'primevue/autocomplete/style';
import { useRouter } from 'vue-router';

const selectedPlayer = ref(null);
const suggestions = ref([]);
const router = useRouter();

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

function onSelect(event) {
  const player = event.value;
  router.push({
    name: 'Player',
    params: { id: player.id },
    query: { name: player.name_full }
  });
}
</script>

<style scoped>
</style>
