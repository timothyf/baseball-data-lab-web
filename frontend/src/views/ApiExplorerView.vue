<template>
  <section class="api-explorer">
    <h2>Frontend API Explorer</h2>
    <div class="frontend explorer-container">
      <div class="explorer-main">
        <div v-if="endpoints.length">
          <label for="endpoint-select">Endpoint:</label>
          <select id="endpoint-select" v-model="selected">
            <option :value="null" disabled>Select an endpoint</option>
            <option v-for="ep in endpoints" :key="ep.template" :value="ep">
              {{ ep.path }}
            </option>
          </select>
          <div v-if="selected">
            <div v-for="param in selected.params" :key="param" class="param-input">
              <label :for="param">{{ param }}</label>
              <input :id="param" v-model="params[param]" />
            </div>
            <div v-if="selected.query_params && selected.query_params.length" class="query-input">
              <label for="query">Query</label>
              <input id="query" :placeholder="queryPlaceholder" v-model="query" />
            </div>
            <button @click="callEndpoint">Fetch</button>
          </div>
          <div v-if="result">
            <pre v-if="resultType === 'json' || resultType === 'text'">{{ result }}</pre>
            <img v-else-if="resultType === 'image'" :src="result" alt="Response image" />
            <a v-else :href="result" download>Download result</a>
          </div>
        </div>
      </div>
      <aside class="explorer-sidebar">
        <h3>Sample IDs</h3>
        <h4>Players</h4>
        <ul>
          <li v-for="p in samplePlayers" :key="p.id">{{ p.name }} - {{ p.id }}</li>
        </ul>
        <h4>Teams</h4>
        <ul>
          <li v-for="t in sampleTeams" :key="t.id">{{ t.name }} - {{ t.id }}</li>
        </ul>
      </aside>
    </div>
    <h2>Backend API Explorer</h2>
    <p>This section allows you to explore the backend API endpoints. BaseballDataLab provides a unified 
       interface to access various baseball data.</p>
    <div class="backend explorer-container">
      <div class="explorer-main"></div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';

const endpoints = ref([]);
const selected = ref(null);
const params = ref({});
const query = ref('');
const result = ref(null);
const resultType = ref('');

const queryPlaceholder = computed(() => {
  if (!selected.value || !selected.value.query_params || !selected.value.query_params.length) {
    return 'param=value';
  }
  return `${selected.value.query_params.map((p) => `${p}=value`).join('&')}`;
});

const samplePlayers = [
  { id: 669373, name: 'Tarik Skubal' },
  { id: 682928, name: 'Riley Greene' },
  { id: 545361, name: 'Mike Trout' },
  { id: 605141, name: 'Mookie Betts' },
  { id: 592450, name: 'Aaron Judge' },
  { id: 621043, name: 'Shohei Ohtani' },
  { id: 694973, name: 'Paul Skenes' }
];

const sampleTeams = [
  { id: 116, name: 'Detroit Tigers' },
  { id: 117, name: 'Houston Astros' },
  { id: 118, name: 'Kansas City Royals' },
  { id: 147, name: 'New York Yankees' },
  { id: 108, name: 'Los Angeles Angels' },
  { id: 119, name: 'Los Angeles Dodgers' }
];

onMounted(async () => {
  try {
    const res = await fetch('/api/endpoints/');
    if (res.ok) {
      const data = await res.json();
      endpoints.value = data.endpoints || [];
    }
  } catch (e) {
    // ignore
  }
});

watch(selected, () => {
  if (resultType.value === 'image' && result.value) {
    URL.revokeObjectURL(result.value);
  }
  params.value = {};
  query.value = '';
  result.value = null;
  resultType.value = '';
});

async function callEndpoint() {
  if (!selected.value) return;
  let url = selected.value.template;
  for (const [key, val] of Object.entries(params.value)) {
    url = url.replace(new RegExp(`<[^:>]+:${key}>`), encodeURIComponent(val));
  }
  if (query.value) {
    url += `?${query.value}`;
  }
  const resp = await fetch(url);
  const contentType = resp.headers.get('Content-Type') || '';
  resultType.value = '';
  if (contentType.includes('application/json')) {
    const data = await resp.json();
    result.value = JSON.stringify(data, null, 2);
    resultType.value = 'json';
  } else if (contentType.startsWith('text/')) {
    result.value = await resp.text();
    resultType.value = 'text';
  } else if (contentType.startsWith('image/')) {
    const blob = await resp.blob();
    result.value = URL.createObjectURL(blob);
    resultType.value = 'image';
  } else {
    const blob = await resp.blob();
    result.value = URL.createObjectURL(blob);
    resultType.value = 'blob';
  }
}
</script>

<style scoped>
.api-explorer {
  max-width: 1284px;
}
.explorer-container {
  display: flex;
}
.explorer-main {
  flex: 1;
}
.explorer-sidebar {
  margin-left: 2rem;
  max-width: 250px;
}
.param-input,
.query-input {
  margin-top: 1rem;
}
pre {
  margin-top: 1rem;
  background: #f5f5f5;
  padding: 1rem;
  overflow: auto;
}
</style>
