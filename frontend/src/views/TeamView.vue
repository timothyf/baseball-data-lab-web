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

    <div v-if="recentSchedule">
      <div class="schedule-section">
        <h2>Previous Games</h2>
        <ul>
          <li v-for="game in previousGames" :key="`prev-` + game.gamePk">
            {{ formatDate(game.gameDate) }} {{ describeGame(game, true) }}
          </li>
        </ul>
      </div>
      <div class="schedule-section">
        <h2>Upcoming Games</h2>
        <ul>
          <li v-for="game in nextGames" :key="`next-` + game.gamePk">
            {{ formatDate(game.gameDate) }} {{ describeGame(game, false) }}
          </li>
        </ul>
      </div>
    </div>
    <div v-else>
      <p>Loading schedule…</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue';

const { id, name } = defineProps({
  id: { type: [String, Number], required: true },
  name: { type: String, required: true }
});

const teamLogoSrc = ref("");
const teamRecord = ref(null);
const recentSchedule = ref(null);

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
  loadRecentSchedule(id);
});

watch(() => id, (newId) => {
  loadLogo(newId);
  loadRecord(newId);
  loadRecentSchedule(newId);
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

async function loadRecentSchedule(teamId) {
  try {
    const res = await fetch(`/api/teams/${teamId}/recent_schedule/`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    recentSchedule.value = await res.json();
  } catch (e) {
    console.error("Failed to fetch recent schedule:", e);
    recentSchedule.value = null;
  }
}

const previousGames = computed(() => {
  const dates = recentSchedule.value?.previousGameSchedule?.dates ?? [];
  return dates.flatMap(d => d.games);
});

const nextGames = computed(() => {
  const dates = recentSchedule.value?.nextGameSchedule?.dates ?? [];
  return dates.flatMap(d => d.games);
});

const mlbamTeamId = computed(() => recentSchedule.value?.id);

function formatDate(dateStr) {
  const d = new Date(dateStr);
  return isNaN(d) ? dateStr : d.toLocaleDateString();
}

function describeGame(game, includeScore) {
  const teamId = mlbamTeamId.value;
  const home = game.teams.home;
  const away = game.teams.away;
  const isHome = home.team.id === teamId;
  const opponent = isHome ? away.team.name : home.team.name;
  const vsAt = isHome ? 'vs' : '@';
  let result = '';
  if (includeScore && home.score != null && away.score != null) {
    const usScore = isHome ? home.score : away.score;
    const oppScore = isHome ? away.score : home.score;
    const outcome = usScore > oppScore ? 'W' : (usScore < oppScore ? 'L' : 'T');
    result = ` ${outcome} ${usScore}-${oppScore}`;
  }
  return `${vsAt} ${opponent}${result}`;
}
</script>

<style scoped>

.team-header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  padding: 50px;
  font-family: proxima-nova, 'open Sans', Helvetica, Arial, sans-serif;
}

.team-logo {
  width: 120px;
  height: auto;
  margin-right: 5rem;
}

.team-info h1 {
  margin: 0;
  font-size: 55px;
  font-weight: 700;
}

.team-info p {
  margin: 0;
  font-size: 35px;
  font-weight: 600;
  color: #555;
  padding-top: 8px;
}

.schedule-section {
  margin-top: 1rem;
}

.schedule-section ul {
  list-style: none;
  padding-left: 0;
}

.schedule-section li {
  margin-bottom: 0.25rem;
}

</style>
