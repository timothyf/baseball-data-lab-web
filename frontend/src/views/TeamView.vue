<template>
  <section class="team-view" :style="teamColorStyle">
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
        </div>
      </div>
      <TabView>
        <TabPanel header="Summary">
          <div class="summary-content">
            <p v-if="teamRecord">
              {{ teamRecord.wins }}-{{ teamRecord.losses }} -
              {{ formatRank(teamRecord.divisionRank) }}
            </p>
            <p v-else>Loading data...</p>
            <p class="venue-name" v-if="teamDetails">
              {{ teamDetails.venue?.name }} • {{ teamDetails.location_name }}
            </p>
          </div>
          <div v-if="divisionStandings.length" class="stats-container">
            <table class="team-stats division-standings">
              <thead>
                <tr>
                  <th>Team</th>
                  <th>W</th>
                  <th>L</th>
                  <th>PCT</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="record in divisionStandings"
                  :key="record.team.id"
                  :class="{ 'current-team': record.team.id === mlbamTeamId }"
                >
                  <td>{{ record.team.name }}</td>
                  <td>{{ record.wins }}</td>
                  <td>{{ record.losses }}</td>
                  <td>{{ record.winningPercentage }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </TabPanel>

        <TabPanel header="Leaders">
          <div v-if="leaders" class="leader-cards">
          <div v-if="leaders.batting || leaders.pitching" class="leaders-section">
            <div v-if="leaders.batting" class="stats-container">
              <h2>Batting Leaders</h2>
              <ul>
                <li v-for="(data, stat) in leaders.batting" :key="`bat-` + stat">
                  {{ stat }}:
                  <RouterLink
                    :to="{ name: 'Player', params: { id: data.id }, query: { name: data.name } }"
                  >
                    {{ data.name }}
                  </RouterLink>
                  {{ ['AVG','SLG','OPS'].includes(stat) && data.value != null ? parseFloat(data.value).toFixed(3).replace(/^0\./, '.') : data.value }}
                </li>
              </ul>
            </div>
            <div v-if="leaders.pitching" class="stats-container">
              <h2>Pitching Leaders</h2>
              <ul>
                <li v-for="(data, stat) in leaders.pitching" :key="`pit-` + stat">
                  {{ stat }}:
                  <RouterLink
                    :to="{ name: 'Player', params: { id: data.id }, query: { name: data.name } }"
                  >
                    {{ data.name }}
                  </RouterLink>
                    {{ stat === 'ERA' && data.value != null ? parseFloat(data.value).toFixed(2) : data.value }}
                </li>
              </ul>
            </div>
          </div>
          </div>
        </TabPanel>

        <TabPanel header="Roster">
          <div v-if="batters.length || pitchers.length" class="roster-section">
            <div v-if="batters.length" class="stats-container roster">
              <h2>Batters ({{ batters.length }})</h2>
              <table class="team-stats roster-table">
                <thead class="roster-head">
                  <tr>
                    <th>Name</th>
                    <th>Age</th>
                    <th>Pos</th>
                    <th>Bats</th>
                    <th>#</th>
                    <th>MLB ID</th>
                  </tr>
                </thead>
                <tbody>
                  <template v-for="group in battersByPosition" :key="group.position">
                    <tr class="position-row">
                      <th colspan="6">{{ group.position }}</th>
                    </tr>
                    <tr v-for="player in group.players" :key="player.person.id">
                      <td>
                        <RouterLink :to="{ name: 'Player', params: { id: player.person.id } }">
                          {{ player.person.fullName }}
                        </RouterLink>
                      </td>
                      <td>{{ player.person?.currentAge ?? '' }}</td>
                      <td>{{ player.position.abbreviation }}</td>
                      <td>{{ player.person?.batSide?.code ?? '' }}</td>
                      <td>{{ player.person?.primaryNumber ?? '' }}</td>
                      <td>
                        <a
                          :href="`https://www.mlb.com/player/${player.person.id}`"
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          {{ player.person.id ?? '' }}
                        </a>
                      </td>
                    </tr>
                  </template>
                </tbody>
              </table>
            </div>

            <div v-if="pitchers.length" class="stats-container roster">
              <h2>Pitchers ({{ pitchers.length }})</h2>
              <table class="team-stats roster-table">
                <thead class="roster-head">
                  <tr>
                    <th>Name</th>
                    <th>Age</th>
                    <th>Throws</th>
                    <th>#</th>
                    <th>MLB ID</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="player in pitchers" :key="player.person.id">
                    <td>
                      <RouterLink :to="{ name: 'Player', params: { id: player.person.id } }">
                        {{ player.person.fullName }}
                      </RouterLink>
                    </td>
                    <td>{{ player.person?.currentAge ?? '' }}</td>
                    <td>{{ player.person?.pitchHand?.code ?? '' }}</td>
                    <td>{{ player.person?.primaryNumber ?? '' }}</td>
                    <td>
                      <a
                        :href="`https://www.mlb.com/player/${player.person.id}`"
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        {{ player.person.id ?? '' }}
                      </a>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </TabPanel>

        <TabPanel header="Stats">
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
        </TabPanel>

        <TabPanel header="Schedule">
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
                    <RouterLink
                      :to="{ name: 'Game', params: { game_pk: game.gamePk } }"
                    >
                      {{ formatDate(game.gameDate) }} {{ describeGame(game, false) }}
                    </RouterLink>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </TabPanel>
      </TabView>
    </div>
  </section>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
import teamColors from '../data/teamColors.json';

const { id, name } = defineProps({
  id: { type: [String, Number], required: true },
  name: { type: String, required: true }
});

const teamLogoSrc = ref("");
const teamRecord = ref(null);
const recentSchedule = ref(null);
const roster = ref([]);
const internalTeamId = ref(null);
const teamDetails = ref(null);
const divisionStandings = ref([]);
const leaders = ref(null);
const mlbamTeamId = computed(() => recentSchedule.value?.id);


const teamColorStyle = computed(() => {
  const colors = teamColors[name] || [];
  return {
    '--color-primary': colors[0]?.hex || '#1e3a8a', // Navy, default: blue
    '--color-secondary': colors[1]?.hex || '#1e40af', // Orange, default: dark blue
    '--color-accent': colors[2]?.hex || '#1e3a8a' // default: blue
  };
});

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
    await loadStandings();
  } catch (e) {
    console.error("Failed to fetch team record:", e);
    teamRecord.value = null;
    divisionStandings.value = [];
  }
}

async function loadStandings() {
  try {
    const res = await fetch(`/api/standings/`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const records = data.records || data;
    const divisionId = teamRecord.value?.divisionId;
    const division = records.find(r => r.division?.id === divisionId);
    divisionStandings.value = division?.teamRecords || [];
  } catch (e) {
    console.error("Failed to fetch standings:", e);
    divisionStandings.value = [];
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
  await loadTeamDetails(internalTeamId.value);
  await loadRecentSchedule(internalTeamId.value);
  await loadRoster(internalTeamId.value);
  await loadLeaders(internalTeamId.value);
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
    teamDetails.value = null;
    divisionStandings.value = [];
    leaders.value = null;
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
      divisionStandings.value = [];
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

async function loadLeaders(teamId) {
  try {
    const res = await fetch(`/api/teams/${teamId}/leaders/`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    leaders.value = await res.json();
  } catch (e) {
    console.error("Failed to fetch team leaders:", e);
    leaders.value = null;
  }
}

async function loadTeamDetails(teamId) {
  try {
    const res = await fetch(`/api/teams/${teamId}/`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    teamDetails.value = await res.json();
  } catch (e) {
    console.error("Failed to fetch team info:", e);
    teamDetails.value = null;
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

const batters = computed(() =>
  roster.value.filter(p => p.position?.abbreviation !== 'P')
);

const pitchers = computed(() =>
  roster.value.filter(p => p.position?.abbreviation === 'P')
);

const battersByPosition = computed(() => {
  const order = ['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'OF', 'DH'];
  const groups = batters.value.reduce((acc, player) => {
    const pos = player.position?.abbreviation || 'Other';
    if (!acc[pos]) acc[pos] = [];
    acc[pos].push(player);
    return acc;
  }, {});
  return Object.keys(groups)
    .sort((a, b) => {
      const ai = order.indexOf(a);
      const bi = order.indexOf(b);
      if (ai === -1 && bi === -1) return a.localeCompare(b);
      if (ai === -1) return 1;
      if (bi === -1) return -1;
      return ai - bi;
    })
    .map((pos) => ({
      position: pos,
      players: groups[pos].sort((a, b) =>
        (a.person?.fullName ?? '').localeCompare(b.person?.fullName ?? '')
      ),
    }));
});

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
  max-width: 1100px;
  margin: 0 auto;
}

  .team-info p.venue-name {
    font-size: 22px;
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

.roster-section {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.leader-cards {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-top: 1rem;
}

.leader-card {
  flex: 1 1 45%;
}

.roster {
  flex: 1 1 45%;
  margin: 0 auto 1rem;
  padding: 0.5rem;
}

.roster-table {
  font-size: 1.2rem;
}

.roster-table th,
.roster-table td {
  padding: 0.25rem 0.5rem;
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

.roster-head tr th {
  color: white;
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

.division-standings .current-team {
  background-color: var(--color-accent);
  color: var(--color-primary);
  font-weight: 600;
}

.position-row th {
  background-color: var(--color-secondary);
  color: #fff;
  text-align: left;
}

</style>
