<template>
  <AutoComplete
    v-model="selected"
    :suggestions="suggestions"
    @complete="search"
    @item-select="onSelect"
    :optionLabel="optionLabel"
    :placeholder="placeholder"
  >
    <template #option="{ option }">
      <div>
        {{ option[optionLabel] }}
        <span v-if="option.team_name"> - {{ option.team_name }}</span>
      </div>
    </template>
  </AutoComplete>
</template>

<script setup>
import { ref } from 'vue';
import AutoComplete from 'primevue/autocomplete';
import 'primevue/autocomplete/style';
import { useRouter } from 'vue-router';

const props = defineProps({
  placeholder: {
    type: String,
    required: true
  },
  optionLabel: {
    type: String,
    required: true
  },
  searchEndpoint: {
    type: String,
    required: true
  },
  routeName: {
    type: String,
    required: true
  },
  idField: {
    type: String,
    default: 'id'
  }
});

const selected = ref(null);
const suggestions = ref([]);
const router = useRouter();

async function search(event) {
  const query = event.query;
  if (!query) {
    suggestions.value = [];
    return;
  }
  try {
    const resp = await fetch(`${props.searchEndpoint}?q=${encodeURIComponent(query)}`);
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
  const item = event.value;
  const routeId = item[props.idField];
  router.push({
    name: props.routeName,
    params: { id: routeId },
    query: { name: item[props.optionLabel] }
  });
}
</script>

<style scoped>
</style>

