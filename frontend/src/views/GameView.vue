<template>
  <section class="game-view" :style="pageStyle">
    <div v-if="game" class="game-container">
      <h2 class="matchup-header">
        <img :src="game.away_team_data.logo_url" alt="Away Logo" class="team-logo" />
        {{ game.away_team_data.name }} @
        <img :src="game.home_team_data.logo_url" alt="Home Logo" class="team-logo" />
        {{ game.home_team_data.name }}
      </h2>
      <h3 class="game-date">{{ game.gameDate }}</h3>
      <div class="game-summary">
        <div v-if="innings.length" class="card linescore-div">
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
                <th :style="{ backgroundColor: awayColor }">{{ game.away_team_data.name }}</th>
                <td v-for="inning in innings" :key="`away-` + inning.num">{{ inning.away?.runs ?? '' }}</td>
                <td>{{ linescoreTeams.away?.runs ?? '' }}</td>
                <td>{{ linescoreTeams.away?.hits ?? '' }}</td>
                <td>{{ linescoreTeams.away?.errors ?? '' }}</td>
              </tr>
              <tr>
                <th :style="{ backgroundColor: homeColor }">{{ game.home_team_data.name }}</th>
                <td v-for="inning in innings" :key="`home-` + inning.num">{{ inning.home?.runs ?? '' }}</td>
                <td>{{ linescoreTeams.home?.runs ?? '' }}</td>
                <td>{{ linescoreTeams.home?.hits ?? '' }}</td>
                <td>{{ linescoreTeams.home?.errors ?? '' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="summary-info card">
          <p>Winning Pitcher: {{ winningPitcher }}</p>
          <p>Losing Pitcher: {{ losingPitcher }}</p>
          <p>HRs: {{ homers }}</p>
          <p>Attendance: {{ attendance }}</p>
          <p>Game Time: {{ gameDuration }}</p>
        </div>
      </div>
        <div v-if="boxscore" class="boxscore">
          <h3>Boxscore</h3>
          <div v-for="side in ['away', 'home']" :key="side" class="team-boxscore card">
            <h4>{{ side === 'away' ? game.away_team_data.name : game.home_team_data.name }}</h4>
            <table class="boxscore-table" :style="{ '--team-color': side === 'away' ? awayColor : homeColor }">
              <thead>
                <tr>
                  <th>Batter</th>
                  <th>AB</th>
                  <th>R</th>
                  <th>H</th>
                  <th>RBI</th>
                  <th>BB</th>
                  <th>SO</th>
                  <th>AVG</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="id in (boxscoreTeams[side]?.batters ?? [])
                    .filter(id => playerStat(side, id, 'batting', 'plateAppearances') > 0)"
                  :key="`bat-` + id"
                >
                  <td>{{ playerName(side, id) }}</td>
                  <td>{{ playerStat(side, id, 'batting', 'atBats') }}</td>
                  <td>{{ playerStat(side, id, 'batting', 'runs') }}</td>
                  <td>{{ playerStat(side, id, 'batting', 'hits') }}</td>
                  <td>{{ playerStat(side, id, 'batting', 'rbi') }}</td>
                  <td>{{ playerStat(side, id, 'batting', 'baseOnBalls') }}</td>
                  <td>{{ playerStat(side, id, 'batting', 'strikeOuts') }}</td>
                  <td>{{ playerSeasonStat(side, id, 'batting', 'avg') }}</td>
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
                  <th>ERA</th>
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
                  <td>{{ playerSeasonStat(side, id, 'pitching', 'era') }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import teamColors from '../data/teamColors.json';

const { game_pk } = defineProps({
  game_pk: { type: [String, Number], required: true }
});

const game = ref(null);
const homeColor = ref('#ffffff');
const awayColor = ref('#ffffff');

onMounted(async () => {
  const resp = await fetch(`/api/games/${game_pk}/`);
  if (resp.ok) {
    game.value = await resp.json();
    const awayColors = teamColors[game.value.away_team_data.name] || [];
    awayColor.value = awayColors[0]?.hex || '#ffffff';
    const homeColors = teamColors[game.value.home_team_data.name] || [];
    homeColor.value = homeColors[0]?.hex || '#ffffff';
  }

});

const pageStyle = computed(() => ({
  '--color-primary': homeColor.value,
  '--color-secondary': awayColor.value
}));



const homeScore = computed(() => game.value?.teams?.home?.score ?? '');
const awayScore = computed(() => game.value?.teams?.away?.score ?? '');

const innings = computed(() => game.value?.scoreboard?.linescore?.innings ?? []);
const linescoreTeams = computed(() => game.value?.scoreboard?.linescore?.teams ?? {});

const boxscore = computed(() => game.value?.boxscore ?? game.value?.liveData?.boxscore);
const boxscoreTeams = computed(() => boxscore.value?.teams ?? {});

const winningPitcher = computed(() =>
  game.value?.summary?.winningPitcher ||
  game.value?.liveData?.decisions?.winner?.fullName ||
  '—'
);

const losingPitcher = computed(() =>
  game.value?.summary?.losingPitcher ||
  game.value?.liveData?.decisions?.loser?.fullName ||
  '—'
);

const homers = computed(() => {
  const fromSummary = game.value?.summary?.homers;
  if (fromSummary && fromSummary.length) {
    return fromSummary.join(', ');
  }
  const info = game.value?.liveData?.boxscore?.info ?? [];
  const hrEntry = info.find(item => item.label === 'HR');
  return hrEntry ? hrEntry.value : '—';
});

const attendance = computed(() => {
  const att =
    game.value?.summary?.attendance ??
    (game.value?.liveData?.boxscore?.info || []).find(i => i.label === 'Att')?.value;
  if (!att) return '—';
  return typeof att === 'number' ? att.toLocaleString() : att;
});

const gameDuration = computed(() => {
  return (
    game.value?.summary?.duration ||
    (game.value?.liveData?.boxscore?.info || []).find(i => i.label === 'T')?.value ||
    '—'
  );
});

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

function playerSeasonStat(side, id, statType, field) {
  const p = player(side, id);
  return p.seasonStats?.[statType]?.[field] ?? '';
}

</script>

<style scoped>
.game-view {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  padding: 2rem 1rem;
}

.game-container {
  max-width: 1200px;
  margin: 0 auto;
}

.matchup-header {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
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
  color: #000;
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
  margin-top: 20px;
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
  color: #000;
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
  color: #000;
}

.game-date {
  font-size: 1.4rem;
  color: #fff;
  margin: 0 0 1rem;
  text-align: center;
}

.game-summary {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: 1rem;
}

.summary-info {
  flex: 1;
}
</style>
