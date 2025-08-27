<template>
  <div class="api-explorer-wrapper">
    <section class="api-explorer">
      <h2 class="explorer-title frontend">Frontend API Explorer</h2>
      <div class="frontend explorer-container">
        <div class="explorer-main">
          <div v-if="endpoints.length">
            <label for="endpoint-select">Endpoint: </label>
            <select id="endpoint-select" v-model="selected">
              <option :value="null" disabled>Select an endpoint</option>
              <option v-for="ep in endpoints" :key="ep.template" :value="ep"> {{ ep.path }} </option>
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
              <JsonViewer v-if="resultType === 'json'" :data="result" />
              <pre v-else-if="resultType === 'text'">{{ result }}</pre>
              <img v-else-if="resultType === 'image'" :src="result" alt="Response image" />
              <a v-else :href="result" download>Download result</a>
            </div>
          </div>
        </div>
      </div>
      <h2 class="explorer-title backend">Backend API Explorer</h2>
      <div class="backend explorer-container">
        <div class="explorer-main">
          <p>UnifiedDataClient:</p>
          <div v-if="backendMethods.length">
            <label for="method-select">Method: </label>
            <select id="method-select" v-model="backendSelected">
              <option :value="null" disabled>Select a method</option>
              <option v-for="m in backendMethods" :key="m.name" :value="m">{{ m.name }}</option>
            </select>
              <div v-if="backendSelected">
                <div v-for="param in backendParsedParams" :key="param.name" class="param-input">
                  <label :for="`backend-${param.name}`">{{ param.label }}: </label>
                  <input :id="`backend-${param.name}`" v-model="backendParams[param.name]" />
                </div>
                <button @click="callBackend">Fetch</button>
              </div>
            <div v-if="backendResult">
              <JsonViewer v-if="backendResultType === 'json'" :data="backendResult" />
              <pre v-else-if="backendResultType === 'text'">{{ backendResult }}</pre>
              <img v-else-if="backendResultType === 'image'" :src="backendResult" alt="Response image" />
              <a v-else :href="backendResult" download>Download result</a>
            </div>
          </div>
        </div>
      </div>
    </section>
    <aside class="explorer-sidebar">
      <h3>Sample IDs</h3>
      <h4>Players</h4>
      <ul>
        <li
          v-for="p in samplePlayers"
          :key="p.id"
          @click="copyId(p.id)"
        >
          {{ p.name }} - {{ p.id }}
        </li>
      </ul>
      <h4>Teams</h4>
      <ul>
        <li
          v-for="t in sampleTeams"
          :key="t.id"
          @click="copyId(t.id)"
        >
          {{ t.name }} - {{ t.id }}
        </li>
      </ul>
      <h4>Game PKs</h4>
      <ul>
        <li
          v-for="g in sampleGames"
          :key="g.id"
          @click="copyId(g.id)"
        >
          {{ g.name }} - {{ g.id }}
        </li>
      </ul>
    </aside>
  </div>
</template>
<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import JsonViewer from '../components/JsonViewer.vue';

const endpoints = ref([]);
const selected = ref(null);
const params = ref({});
const query = ref('');
const result = ref(null);
const resultType = ref('');

const backendMethods = ref([]);
const backendSelected = ref(null);
const backendParams = ref({});
const backendResult = ref(null);
const backendResultType = ref('');
const backendParsedParams = computed(() => {
  if (!backendSelected.value) return [];
  return backendSelected.value.params.map((p) => {
    const [name, def] = p.split('=');
    let defaultVal = def ?? '';
    if (defaultVal.startsWith("'") && defaultVal.endsWith("'")) {
      defaultVal = defaultVal.slice(1, -1);
    }
    return { name, label: name, default: defaultVal };
  });
});

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

const sampleGames = [
  { id: 746865, name: 'Cardinals at Cubs (2024-06-15)' },
  { id: 744925, name: 'Guardians at Blue Jays (2024-06-15)' },
  { id: 745329, name: 'Angels at Giants (2024-06-15)' },
  { id: 747024, name: 'Phillies at Orioles (2024-06-15)' },
  { id: 744846, name: 'Marlins at Nationals (2024-06-15)' },
  { id: 746381, name: 'Tigers at Astros (2024-06-15)' },
  { id: 745805, name: 'Padres at Mets (2024-06-15)' }
];

function copyId(id) {
  navigator.clipboard?.writeText(String(id));
}

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
  try {
    const res = await fetch('/api/unified/methods/');
    if (res.ok) {
      const data = await res.json();
      backendMethods.value = data.methods || [];
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

watch(backendSelected, () => {
  if (backendResultType.value === 'image' && backendResult.value) {
    URL.revokeObjectURL(backendResult.value);
  }
  backendParams.value = {};
  backendResult.value = null;
  backendResultType.value = '';
  if (backendSelected.value) {
    for (const p of backendParsedParams.value) {
      backendParams.value[p.name] = p.default;
    }
  }
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
    result.value = await resp.json();
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

async function callBackend() {
  if (!backendSelected.value) return;
  if (backendResultType.value === 'image' && backendResult.value) {
    URL.revokeObjectURL(backendResult.value);
  }
  const query = new URLSearchParams();
  for (const [k, v] of Object.entries(backendParams.value)) {
    if (v !== '') query.append(k, v);
  }
  const url = `/api/unified/${backendSelected.value.name}/?${query.toString()}`;
  const resp = await fetch(url);
  const contentType = resp.headers.get('Content-Type') || '';
  backendResultType.value = '';
  if (contentType.includes('application/json')) {
    backendResult.value = await resp.json();
    backendResultType.value = 'json';
  } else if (contentType.startsWith('text/')) {
    backendResult.value = await resp.text();
    backendResultType.value = 'text';
  } else if (contentType.startsWith('image/')) {
    const blob = await resp.blob();
    backendResult.value = URL.createObjectURL(blob);
    backendResultType.value = 'image';
  } else {
    const blob = await resp.blob();
    backendResult.value = URL.createObjectURL(blob);
    backendResultType.value = 'blob';
  }
}
</script>
<style scoped>
.api-explorer-wrapper {
  display: flex;
  flex-direction: row;;
  justify-content: space-around;
}

.api-explorer {

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

.explorer-sidebar ul {
  list-style: none;
  padding: 0;
}

.explorer-sidebar li {
  cursor: pointer;
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

.explorer-title.backend {
  margin-top: 80px;
  margin-bottom: 10px;
}
</style>
