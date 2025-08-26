<template>
  <section class="api-explorer">
    <h2>API Explorer</h2>
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
        <div class="query-input">
          <label for="query">Query</label>
          <input id="query" placeholder="e.g., date=2024-04-01" v-model="query" />
        </div>
        <button @click="callEndpoint">Fetch</button>
      </div>
      <div v-if="result">
        <pre v-if="resultType === 'json' || resultType === 'text'">{{ result }}</pre>
        <img v-else-if="resultType === 'image'" :src="result" alt="Response image" />
        <a v-else :href="result" download>Download result</a>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';

const endpoints = ref([]);
const selected = ref(null);
const params = ref({});
const query = ref('');
const result = ref(null);
const resultType = ref('');

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
  padding: 2rem;
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
