<template>
  <div>
    <h1>{{ name }}</h1>

    <img v-if="teamLogoSrc" :src="teamLogoSrc" alt="Team Logo" />
    <p v-else>Loading logo…</p>

    <p>ID: {{ id }}</p>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';

const { id, name } = defineProps({
  id: { type: [String, Number], required: true },
  name: { type: String, required: true }
});

const teamLogoSrc = ref("");

// fetcher for plain-text URL
async function loadLogo(teamId) {
  try {
    const res = await fetch(`/api/teams/${teamId}/logo/`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const url = (await res.text()).trim();   // <- plain text, not JSON
    teamLogoSrc.value = url || "";           // handle empty response
  } catch (e) {
    console.error("Failed to fetch logo:", e);
    teamLogoSrc.value = "";
  }
}

onMounted(() => loadLogo(id));
watch(() => id, (newId) => loadLogo(newId));
</script>

<style scoped>
img { max-width: 200px; height: auto; }
</style>
