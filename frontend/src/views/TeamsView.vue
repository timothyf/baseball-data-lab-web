

<template>
  <div>
    <h1>Teams</h1>
    <AutoComplete
      v-model="selectedTeam"
      :suggestions="suggestions"
      @complete="searchTeams"
      @item-select="onSelect"
      optionLabel="full_name"
      placeholder="Search for a team"
    >
      <template #option="{ option }">
        <div>{{ option.full_name }}</div>
      </template>
    </AutoComplete>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import AutoComplete from 'primevue/autocomplete';
import 'primevue/autocomplete/style';
import { useRouter } from 'vue-router';

const selectedTeam = ref(null);
const suggestions = ref([]);
const router = useRouter();

async function searchTeams(event) {
  const query = event.query;
  if (!query) {
    suggestions.value = [];
    return;
  }
  try {
    const resp = await fetch(`/api/teams/?q=${encodeURIComponent(query)}`);
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
  const team = event.value;
  router.push({
    name: 'Team',
    params: { id: team.id },
    query: { name: team.full_name }
  });
}
</script>

<style scoped>
</style>
