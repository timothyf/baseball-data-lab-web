<template>
  <div>
    <div v-if="game">
      <h2 class="matchup-header" :style="headerStyle">
        <img :src="awayLogo" alt="Away Logo" class="team-logo" />
        {{ awayTeam }} @
        <img :src="homeLogo" alt="Home Logo" class="team-logo" />
        {{ homeTeam }}
      </h2>
      <h3 class="game-date">{{ game.gameDate }}</h3>
      <div v-if="innings.length" class="card">
        <table class="linescore" :style="{ '--team-color': '#f0f0f0' }">
          <thead>
            <tr>
              <th></th>
              <th v-for="inning in innings" :key="inning.num">{{ inning.num }}</th>
              <th>R</th>
              <th>H</th>
              <th>E</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th :style="{ backgroundColor: awayColor }">{{ awayTeam }}</th>
              <td v-for="inning in innings" :key="`away-` + inning.num">{{ inning.away?.runs ?? '' }}</td>
              <td>{{ linescoreTeams.away?.runs ?? '' }}</td>
              <td>{{ linescoreTeams.away?.hits ?? '' }}</td>
              <td>{{ linescoreTeams.away?.errors ?? '' }}</td>
            </tr>
            <tr>
              <th :style="{ backgroundColor: homeColor }">{{ homeTeam }}</th>
              <td v-for="inning in innings" :key="`home-` + inning.num">{{ inning.home?.runs ?? '' }}</td>
              <td>{{ linescoreTeams.home?.runs ?? '' }}</td>
              <td>{{ linescoreTeams.home?.hits ?? '' }}</td>
              <td>{{ linescoreTeams.home?.errors ?? '' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
        <div v-if="boxscore" class="boxscore">
          <h3>Boxscore</h3>
          <div v-for="side in ['away', 'home']" :key="side" class="team-boxscore card">
            <h4>{{ side === 'away' ? awayTeam : homeTeam }}</h4>
            <table class="boxscore-table" :style="{ '--team-color': side === 'away' ? awayColor : homeColor }">
              <thead>
                <tr>
                  <th>Batter</th>
                  <th>AB</th>
                  <th>R</th>
                  <th>H</th>
                  <th>RBI</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="id in boxscoreTeams[side]?.batters ?? []" :key="`bat-` + id">
                  <td>{{ playerName(side, id) }}</td>
                  <td>{{ playerStat(side, id, 'batting', 'atBats') }}</td>
                  <td>{{ playerStat(side, id, 'batting', 'runs') }}</td>
                  <td>{{ playerStat(side, id, 'batting', 'hits') }}</td>
                  <td>{{ playerStat(side, id, 'batting', 'rbi') }}</td>
                </tr>
              </tbody>
            </table>
            <table class="boxscore-table" :style="{ '--team-color': side === 'away' ? awayColor : homeColor }">
              <thead>
                <tr>
                  <th>Pitcher</th>
                  <th>IP</th>
                  <th>H</th>
                  <th>R</th>
                  <th>ER</th>
                  <th>BB</th>
                  <th>K</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="id in boxscoreTeams[side]?.pitchers ?? []" :key="`pit-` + id">
                  <td>{{ playerName(side, id) }}</td>
                  <td>{{ playerStat(side, id, 'pitching', 'inningsPitched') }}</td>
                  <td>{{ playerStat(side, id, 'pitching', 'hits') }}</td>
                  <td>{{ playerStat(side, id, 'pitching', 'runs') }}</td>
                  <td>{{ playerStat(side, id, 'pitching', 'earnedRuns') }}</td>
                  <td>{{ playerStat(side, id, 'pitching', 'baseOnBalls') }}</td>
                  <td>{{ playerStat(side, id, 'pitching', 'strikeOuts') }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';

const { game_pk } = defineProps({
  game_pk: { type: [String, Number], required: true }
});

const game = ref(null);
const homeColor = ref('#ffffff');
const awayColor = ref('#ffffff');
const homeLogo = ref('');
const awayLogo = ref('');

onMounted(async () => {
  const resp = await fetch(`/api/games/${game_pk}/`);
  if (resp.ok) {
    game.value = await resp.json();
  }

  // fetch team names
  const homeTeamId = game.value.team_home_id;
  const awayTeamId = game.value.team_away_id;

  if (homeTeamId) {
    const [homeResp, homeLogoResp] = await Promise.all([
      fetch(`/api/teams/${homeTeamId}/`),
      fetch(`/api/teams/${homeTeamId}/logo/`)
    ]);
    if (homeResp.ok) {
      const data = await homeResp.json();
      game.value.homeTeamName = data.full_name;
      homeColor.value = data.primary_color || data.color || '#ffffff';
    }
    if (homeLogoResp.ok) {
      homeLogo.value = (await homeLogoResp.text()).trim();
    }
  }

  if (awayTeamId) {
    const [awayResp, awayLogoResp] = await Promise.all([
      fetch(`/api/teams/${awayTeamId}/`),
      fetch(`/api/teams/${awayTeamId}/logo/`)
    ]);
    if (awayResp.ok) {
      const data = await awayResp.json();
      game.value.awayTeamName = data.full_name;
      awayColor.value = data.primary_color || data.color || '#ffffff';
    }
    if (awayLogoResp.ok) {
      awayLogo.value = (await awayLogoResp.text()).trim();
    }
  }
});

const homeTeam = computed(() => game.value.homeTeamName || '');
const awayTeam = computed(() => game.value.awayTeamName || '');

const headerStyle = computed(() => ({
  background: `linear-gradient(to right, ${awayColor.value}, ${homeColor.value})`,
  color: '#fff',
  padding: '8px',
  borderRadius: '4px',
  textAlign: 'center'
}));



const homeScore = computed(() => game.value?.teams?.home?.score ?? '');
const awayScore = computed(() => game.value?.teams?.away?.score ?? '');

const innings = computed(() => game.value?.scoreboard?.linescore?.innings ?? []);
const linescoreTeams = computed(() => game.value?.scoreboard?.linescore?.teams ?? {});

const boxscore = computed(() => game.value?.boxscore ?? game.value?.liveData?.boxscore);
const boxscoreTeams = computed(() => boxscore.value?.teams ?? {});

function player(side, id) {
  const players = boxscoreTeams.value[side]?.players ?? {};
  const key = `ID${id}`;
  return players[key] || {};
}

function playerName(side, id) {
  const p = player(side, id);
  return p.person?.boxscoreName || p.person?.fullName || '';
}

function playerStat(side, id, statType, field) {
  const p = player(side, id);
  return p.stats?.[statType]?.[field] ?? '';
}
</script>

<style scoped>
.matchup-header {
  display: flex;
  align-items: center;
  justify-content: center;
}

.team-logo {
  width: 32px;
  height: 32px;
  vertical-align: middle;
  margin: 0 8px;
}

.linescore {
  border-collapse: collapse;
}
.linescore thead {
  background-color: var(--team-color);
}
.linescore th,
.linescore td {
  border: 1px solid #ccc;
  text-align: center;
}

.linescore th {
  padding: 8px 12px;
}

.linescore td {
  padding: 4px 8px;
}
.linescore tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

.boxscore {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  width: 100%;
  max-width: 1200px;
  margin: 20px auto 0;
}

.boxscore h3 {
  flex: 0 0 100%; /* always full width */
  margin: 0 0 1rem;
}

.team-boxscore {
  flex: 0 0 49%; /* each takes half width */
  box-sizing: border-box;
  padding: 0.5rem;
}

@media (max-width: 960px) {
  .team-boxscore {
    flex: 0 0 100%;
  }
}

.boxscore-table {
  margin-top: 1rem;
  border-collapse: collapse;
}
.boxscore-table thead {
  background-color: var(--team-color);
}

.boxscore-table th,
.boxscore-table td {
  border: 1px solid #ccc;
  text-align: center;
}

.boxscore-table th {
  padding: 8px 12px;
}

.boxscore-table td {
  padding: 4px 8px;
}
.boxscore-table tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

.card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 16px;
  margin-bottom: 20px;
}

.game-date {
  font-size: 1.2rem;
  color: #555;
  margin: 0 0 1rem;
}
</style>
