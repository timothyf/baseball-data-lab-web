<template>
  <div>
    <h1>{{ name }}</h1>

    <img v-if="teamLogoSrc" :src="teamLogoSrc" alt="Team Logo" />
    <p v-else>Loading logo…</p>

    <div v-if="teamRecord">
      <p>Record: {{ teamRecord.wins }}-{{ teamRecord.losses }}</p>
      <p>Division Rank: {{ teamRecord.divisionRank }}</p>
      <p>Streak: {{ teamRecord.streak?.streakCode }}</p>
    </div>
    <p v-else>Loading record…</p>

  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';

const { id, name } = defineProps({
  id: { type: [String, Number], required: true },
  name: { type: String, required: true }
});

const teamLogoSrc = ref("");
const teamRecord = ref(null);

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

async function loadRecord(teamId) {
  try {
    const res = await fetch(`/api/teams/${teamId}/record/`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    teamRecord.value = await res.json();
  } catch (e) {
    console.error("Failed to fetch team record:", e);
    teamRecord.value = null;
  }
}


onMounted(() => {
  loadLogo(id);
  loadRecord(id);
});

watch(() => id, (newId) => {
  loadLogo(newId);
  loadRecord(newId);
});
</script>

<style scoped>
img { max-width: 200px; height: auto; }
</style>
