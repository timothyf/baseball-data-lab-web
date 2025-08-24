<template>
  <section class="team-view">
    <div class="team-container">
      <div class="team-header">
        <img
          v-if="teamLogoSrc"
          :src="teamLogoSrc"
          alt="Team Logo"
          class="team-logo"
        />

        <div class="team-info">
          <h1>{{ name }}</h1>
          <p v-if="teamRecord">
            {{ teamRecord.wins }}-{{ teamRecord.losses }} -
            {{ formatRank(teamRecord.divisionRank) }}
          </p>
          <p v-else>Loading data...</p>
        </div>
      </div>

      <div v-if="teamRecord" class="stats-container">
        <table class="team-stats">
          <thead>
            <tr>
              <th>Streak</th>
              <th>Last 10</th>
              <th>Last 30</th>
              <th>RS</th>
              <th>RA</th>
              <th>rDiff</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{{ streakCode }}</td>
              <td>{{ lastTen }}</td>
              <td>{{ lastThirty }}</td>
              <td>{{ runsScored }}</td>
              <td>{{ runsAllowed }}</td>
              <td>{{ runDifferential }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="roster.length" class="stats-container">
        <h2>Roster</h2>
        <table class="team-stats">
          <thead>
            <tr>
              <th>Name</th>
              <th>Pos</th>
              <th>G</th>
              <th>AVG</th>
              <th>ERA</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="player in roster" :key="player.person.id">
              <td>
                <RouterLink :to="{ name: 'Player', params: { id: player.person.id } }">
                  {{ player.person.fullName }}
                </RouterLink>
              </td>
              <td>{{ player.position.abbreviation }}</td>
              <td>{{ player.stats?.gamesPlayed ?? '' }}</td>
              <td>{{ player.stats?.avg ?? '' }}</td>
              <td>{{ player.stats?.era ?? '' }}</td>
            </tr>
          </tbody>
        </table>
      </div>

    <div class="recent-schedule" v-if="recentSchedule">
      <div class="schedule-section">
        <h2>Previous Games</h2>
        <div class="schedule-card">
          <ul>
            <li v-for="game in previousGames" :key="`prev-` + game.gamePk">
              <RouterLink
                :to="{ name: 'Game', params: { game_pk: game.gamePk } }"
              >
                {{ formatDate(game.gameDate) }} {{ describeGame(game, true) }}
              </RouterLink>
            </li>
          </ul>
        </div>
      </div>
      <div class="schedule-section">
        <h2>Upcoming Games</h2>
        <div class="schedule-card">
          <ul>
            <li v-for="game in nextGames" :key="`next-` + game.gamePk">
              {{ formatDate(game.gameDate) }} {{ describeGame(game, false) }}
            </li>
          </ul>
        </div>
      </div>
    </div>
    </div>
  </section>
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
const roster = ref([]);
const internalTeamId = ref(null);
const mlbamTeamId = computed(() => recentSchedule.value?.id);

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


async function resolveTeamId(teamId) {
  try {
    const resp = await fetch(`/api/teams/${teamId}/`);
    if (resp.ok) {
      const data = await resp.json();
      internalTeamId.value = data.id;
    } else {
      internalTeamId.value = teamId;
    }
  } catch (e) {
    internalTeamId.value = teamId;
  }
  await loadRecentSchedule(internalTeamId.value);
  await loadRoster(internalTeamId.value);
}

onMounted(() => {
  resolveTeamId(id);
});

watch(
  () => id,
  (newId) => {
    teamLogoSrc.value = "";
    teamRecord.value = null;
    recentSchedule.value = null;
    roster.value = [];
    internalTeamId.value = null;
    resolveTeamId(newId);
  }
);

watch(
  () => mlbamTeamId.value,
  (newId) => {
    if (newId) {
      // team_logo expects the internal team ID, whereas team_record
      // expects the MLBAM team ID. Use the appropriate identifier for
      // each API call.
      loadLogo(internalTeamId.value);
      loadRecord(newId);
    } else {
      teamLogoSrc.value = "";
      teamRecord.value = null;
    }
  }
);

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

async function loadRoster(teamId) {
  try {
    const res = await fetch(`/api/teams/${teamId}/roster/`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    roster.value = data?.roster ?? data ?? [];
  } catch (e) {
    console.error("Failed to fetch roster:", e);
    roster.value = [];
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

const streakCode = computed(() => teamRecord.value?.streak?.streakCode || "");

const lastTen = computed(() => {
  const split = teamRecord.value?.records?.splitRecords?.find(r => r.type === 'lastTen');
  return split ? `${split.wins}-${split.losses}` : "";
});

const lastThirty = computed(() => {
  const split = teamRecord.value?.records?.splitRecords?.find(r => r.type === 'lastThirty');
  return split ? `${split.wins}-${split.losses}` : "";
});

const runsScored = computed(() => teamRecord.value?.runsScored ?? "");
const runsAllowed = computed(() => teamRecord.value?.runsAllowed ?? "");
const runDifferential = computed(() => teamRecord.value?.runDifferential ?? "");

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

.team-view {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  color: #fff;
  padding: 2rem 1rem;
}
.team-container {
  max-width: 800px;
  margin: 0 auto;
}

.team-header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  padding: 3rem;
  font-family: var(--font-base);
  margin: 0 auto;
  max-width: 43.75rem;
  width: 100%;
  text-align: center;
}

.team-logo {
  max-width: 7.5rem;
  width: 100%;
  height: auto;
  margin-right: 5rem;
}

.team-info h1 {
  margin: 0;
  font-size: 3.4rem;
  font-weight: 700;
}

.team-info p {
  margin: 0;
  font-size: 2.2rem;
  font-weight: 600;
  color: var(--color-accent);
  padding-top: 8px;
}

.stats-container {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  padding: 1rem;
  margin: 0 auto 2rem;
  max-width: 100%;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stats-container:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.team-stats {
  border-collapse: collapse;
  font-family: var(--font-base);
  font-size: 1.6rem;
  width: 100%;
}

.team-stats th,
.team-stats td {
  border: 2px solid var(--color-accent);
  padding: 0.5rem 1rem;
  text-align: center;
}

.team-stats th {
  background-color: var(--color-accent);
  color: var(--color-primary);
  font-weight: 600;
}

.recent-schedule {
  display: flex;
  margin: 1rem auto 0;
  justify-content: space-between;
  width: 100%;
  max-width: 700px;
  flex-wrap: wrap;
}

.schedule-section {
  margin: 1rem 0;
  flex: 1 1 45%;
}

.schedule-card {
  background: rgba(255, 255, 255, 0.1);
  padding: 1rem;
  border-radius: 0.5rem;
  margin-top: 1rem;
  text-align: left;
  width: 325px;
}

.schedule-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.schedule-card li {
  margin-bottom: 0.25rem;
}

@media (max-width: 600px) {
  .team-header {
    flex-direction: column;
    padding: 1.5rem 1rem;
  }

  .team-logo {
    margin-right: 0;
    margin-bottom: 1rem;
  }

  .recent-schedule {
    flex-direction: column;
    align-items: center;
  }

  .schedule-section {
    width: 100%;
  }
}

</style>
