<template>
  <div>
    <div class="team-header">
      <img
        v-if="teamLogoSrc"
        :src="teamLogoSrc"
        alt="Team Logo"
        class="team-logo"
      />
      <p v-else>Loading logo…</p>

      <div class="team-info">
        <h1>{{ name }}</h1>
        <p v-if="teamRecord">
          {{ teamRecord.wins }}-{{ teamRecord.losses }} -
          {{ formatRank(teamRecord.divisionRank) }}
        </p>
        <p v-else>Loading record…</p>
      </div>
    </div>

    <div v-if="teamRecord">
      <p>Streak: {{ teamRecord.streak?.streakCode }}</p>
    </div>
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

function formatRank(rank) {
  if (rank == null) return "";
  const j = rank % 10,
    k = rank % 100;
  if (j === 1 && k !== 11) return `${rank}st Place`;
  if (j === 2 && k !== 12) return `${rank}nd Place`;
  if (j === 3 && k !== 13) return `${rank}rd Place`;
  return `${rank}th Place`;
}
</script>

<style scoped>

.team-header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.team-logo {
  width: 120px;
  height: auto;
  margin-right: 1rem;
}

.team-info h1 {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
}

.team-info p {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #555;
}

</style>
