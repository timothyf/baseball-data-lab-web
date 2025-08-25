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
          <h1 v-if="teamRecord">{{ teamRecord.teamName }}</h1>
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
      </div>
      <TabView>
        <TabPanel header="Summary">
          <div class="summary-content">
            <p v-if="teamRecord">
              {{ teamRecord.wins }}-{{ teamRecord.losses }} -
              {{ formatRank(teamRecord.divisionRank) }}
            </p>
            <Skeleton v-else width="200px" height="2rem" />
            <p class="venue-name" v-if="teamDetails">
              {{ teamDetails.venue?.name }} • {{ teamDetails.location_name }}
            </p>
            <Skeleton v-else width="300px" height="1.5rem" />
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
          <div v-else class="leader-cards">
            <Skeleton v-for="n in 2" :key="n" width="45%" height="10rem" />
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
          <div v-else class="roster-section">
            <Skeleton v-for="n in 2" :key="n" class="stats-container roster" height="15rem" />
          </div>
        </TabPanel>

        <TabPanel header="Stats">
          Content coming soon...
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
                    {{ formatDate(game.gameDate) }} {{ describeGame(game, false) }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div v-else class="recent-schedule">
            <Skeleton v-for="n in 2" :key="n" class="schedule-card" height="8rem" width="45%" />
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
import Skeleton from 'primevue/skeleton';
import teamColors from '../data/teamColors.json';
import { useTeamsStore } from '../store/teams';

const { id, name } = defineProps({
  id: { type: [String, Number], required: true },
  name: { type: String, required: true }
});

const teamLogoSrc = ref("");
const teamRecord = ref(null);
const recentSchedule = ref(null);
const roster = ref([]);
const internalTeamId = ref(id);
const teamDetails = ref(null);
const divisionStandings = ref([]);
const leaders = ref(null);
const teamsStore = useTeamsStore();
const deepEqual = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const mlbamTeamId = ref(id);


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
  const cached = teamsStore.getStandings(teamId);
  if (cached) {
    teamRecord.value = cached.record;
    divisionStandings.value = cached.standings;
  }

  const fetchAndUpdate = async () => {
    const recordPromise = fetch(`/api/teams/${teamId}/record/`)
      .then(async (res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .catch((e) => {
        console.error("Failed to fetch team record:", e);
        return null;
      });

    const standingsPromise = loadStandings(teamId).catch((e) => {
      console.error("Failed to fetch standings:", e);
      return [];
    });

    const [record, standings] = await Promise.all([
      recordPromise,
      standingsPromise,
    ]);

    const newData = { record, standings };
    const oldData = teamsStore.getStandings(teamId);
    if (!deepEqual(newData, oldData)) {
      teamsStore.setStandings(teamId, newData);
      if (teamId === mlbamTeamId.value) {
        teamRecord.value = record;
        divisionStandings.value = standings;
      }
    }
  };

  if (cached) {
    fetchAndUpdate();
    return;
  }
  await fetchAndUpdate();
}

async function loadStandings(teamId) {
  const res = await fetch(`/api/standings/`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const data = await res.json();
  const records = data.records || data;
  const division = records.find(r =>
    r.teamRecords?.some(record => record.team.id === Number(teamId))
  );
  return division?.teamRecords || [];
}


async function resolveTeamId(teamId) {
  // Display cached data right away
  loadTeamDetails(teamId).catch(() => {});
  loadRecentSchedule(teamId).catch(() => {});
  loadRoster(teamId).catch(() => {});
  loadLeaders(teamId).catch(() => {});

  // Resolve canonical team ID and revalidate if different
  try {
    const resp = await fetch(`/api/teams/${teamId}/`);
    if (resp.ok) {
      const data = await resp.json();
      const canonical = data.id;
      internalTeamId.value = canonical;
      if (canonical !== teamId) {
        loadTeamDetails(canonical).catch(() => {});
        loadRecentSchedule(canonical).catch(() => {});
        loadRoster(canonical).catch(() => {});
        loadLeaders(canonical).catch(() => {});
      }
    } else {
      internalTeamId.value = teamId;
    }
  } catch (e) {
    internalTeamId.value = teamId;
  }
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
    teamDetails.value = null;
    divisionStandings.value = [];
    leaders.value = null;
    internalTeamId.value = newId;
    mlbamTeamId.value = newId;
    resolveTeamId(newId);
  }
);

watch(
  mlbamTeamId,
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
  },
  { immediate: true }
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
    const data = await res.json();
    recentSchedule.value = data;
    if (data?.id && data.id !== mlbamTeamId.value) {
      mlbamTeamId.value = data.id;
    }
  } catch (e) {
    console.error("Failed to fetch recent schedule:", e);
    recentSchedule.value = null;
  }
}

async function loadRoster(teamId) {
  const cached = teamsStore.getRoster(teamId);
  if (cached) {
    roster.value = cached;
  }

  const fetchAndUpdate = async () => {
    try {
      const res = await fetch(`/api/teams/${teamId}/roster/`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      const parsed = data?.roster ?? data ?? [];
      const oldData = teamsStore.getRoster(teamId);
      if (!deepEqual(parsed, oldData)) {
        teamsStore.setRoster(teamId, parsed);
        if (teamId === internalTeamId.value) {
          roster.value = parsed;
        }
      }
    } catch (e) {
      console.error("Failed to fetch roster:", e);
      if (!cached) {
        roster.value = [];
      }
    }
  };

  if (cached) {
    fetchAndUpdate();
    return;
  }
  await fetchAndUpdate();
}

async function loadLeaders(teamId) {
  const cached = teamsStore.getLeaders(teamId);
  if (cached) {
    leaders.value = cached;
  }

  const fetchAndUpdate = async () => {
    try {
      const res = await fetch(`/api/teams/${teamId}/leaders/`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      const oldData = teamsStore.getLeaders(teamId);
      if (!deepEqual(data, oldData)) {
        teamsStore.setLeaders(teamId, data);
        if (teamId === internalTeamId.value) {
          leaders.value = data;
        }
      }
    } catch (e) {
      console.error("Failed to fetch team leaders:", e);
      if (!cached) {
        leaders.value = null;
      }
    }
  };

  if (cached) {
    fetchAndUpdate();
    return;
  }
  await fetchAndUpdate();
}

async function loadTeamDetails(teamId) {
  const cached = teamsStore.getDetails(teamId);
  if (cached) {
    teamDetails.value = cached;
  }

  const fetchAndUpdate = async () => {
    try {
      const res = await fetch(`/api/teams/${teamId}/`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      const oldData = teamsStore.getDetails(teamId);
      if (!deepEqual(data, oldData)) {
        teamsStore.setDetails(teamId, data);
        if (teamId === internalTeamId.value) {
          teamDetails.value = data;
        }
      }
    } catch (e) {
      console.error("Failed to fetch team info:", e);
      if (!cached) {
        teamDetails.value = null;
      }
    }
  };

  if (cached) {
    fetchAndUpdate();
    return;
  }
  await fetchAndUpdate();
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
  max-width: 1100px;
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
