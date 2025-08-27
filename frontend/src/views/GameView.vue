<template>
  <section class="game-view">
    <div v-if="game" class="game-container">
      <h2 class="matchup-header">
        <img :src="awayTeam.logo_url" alt="Away Logo" class="team-logo" /> {{ awayTeam.name }} @ <img
          :src="homeTeam.logo_url" alt="Home Logo" class="team-logo" /> {{ homeTeam.name }}
      </h2>
      <h3 class="game-date">{{ gameDate }}</h3>
      <div class="game-summary">
        <div v-if="innings.length" class="card linescore-div">
          <table class="linescore">
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
                <th>{{ awayTeam.name }}</th>
                <td v-for="inning in innings" :key="`away-` + inning.num">{{ inning.away?.runs ?? '' }}</td>
                <td>{{ linescoreTeams.away?.runs ?? '' }}</td>
                <td>{{ linescoreTeams.away?.hits ?? '' }}</td>
                <td>{{ linescoreTeams.away?.errors ?? '' }}</td>
              </tr>
              <tr>
                <th>{{ homeTeam.name }}</th>
                <td v-for="inning in innings" :key="`home-` + inning.num">{{ inning.home?.runs ?? '' }}</td>
                <td>{{ linescoreTeams.home?.runs ?? '' }}</td>
                <td>{{ linescoreTeams.home?.hits ?? '' }}</td>
                <td>{{ linescoreTeams.home?.errors ?? '' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="summary-info card">
          <p><span class="title">Winning Pitcher:</span> {{ winningPitcher }}</p>
          <p><span class="title">Losing Pitcher:</span> {{ losingPitcher }}</p>
          <p v-if="savePitcher && savePitcher !== '—'"><span class="title">Save:</span> {{ savePitcher }}</p>
          <p><span class="title">HRs:</span> {{ homers }}</p>
          <p><span class="title">Attendance:</span> {{ attendance }}</p>
          <p><span class="title">Game Time:</span> {{ gameDuration }}</p>
        </div>
      </div>
      <div v-if="topPerformers.length" class="top-performers card">
        <h3>Top Performers</h3>
        <ul>
          <li v-for="tp in topPerformers" :key="tp.player?.person?.id">
            <img
              v-if="teamLogo(tp)"
              :src="teamLogo(tp)"
              alt="Team Logo"
              class="team-logo"
            />
            <span class="player-name">{{ performerName(tp) }}</span>
            <span class="player-summary">{{ performerSummary(tp) }}</span>
          </li>
        </ul>
      </div>
        <div v-if="boxscore" class="boxscore">
          <h3>Boxscore</h3>
          <div v-for="side in ['away', 'home']" :key="side" class="team-boxscore card">
            <h4>{{ side === 'away' ? awayTeam.name : homeTeam.name }}</h4>
            <table class="boxscore-table">
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
            <table class="boxscore-table">
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

const { game_pk } = defineProps({
  game_pk: { type: [String, Number], required: true }
});

const game = ref(null);

const homeTeam = computed(() =>
  game.value?.home_team_data || game.value?.gameData?.teams?.home || {}
);
const awayTeam = computed(() =>
  game.value?.away_team_data || game.value?.gameData?.teams?.away || {}
);
const gameDate = computed(
  () => game.value?.gameDate || game.value?.gameData?.datetime?.originalDate || ''
);

onMounted(async () => {
  const resp = await fetch(`/api/games/${game_pk}/`);
  if (resp.ok) {
    game.value = await resp.json();
  }

});



const homeScore = computed(
  () =>
    game.value?.teams?.home?.score ??
    game.value?.liveData?.linescore?.teams?.home?.runs ??
    ''
);
const awayScore = computed(
  () =>
    game.value?.teams?.away?.score ??
    game.value?.liveData?.linescore?.teams?.away?.runs ??
    ''
);

const innings = computed(
  () =>
    game.value?.scoreboard?.linescore?.innings ??
    game.value?.liveData?.linescore?.innings ??
    []
);
const linescoreTeams = computed(
  () =>
    game.value?.scoreboard?.linescore?.teams ??
    game.value?.liveData?.linescore?.teams ??
    {}
);

const boxscore = computed(() => game.value?.boxscore ?? game.value?.liveData?.boxscore);
const boxscoreTeams = computed(() => boxscore.value?.teams ?? {});

const topPerformers = computed(() => game.value?.topPerformers ?? []);

function performerName(tp) {
  const person = tp?.player?.person || {};
  return person.boxscoreName || person.fullName || '';
}

function performerSummary(tp) {
  return (
    tp?.player?.stats?.batting?.summary ||
    tp?.player?.stats?.pitching?.summary ||
    ''
  );
}

function teamLogo(tp) {
  return tp?.team?.logo_url || tp?.team?.logo || '';
}

function pitcherName(entry) {
  if (!entry) return '';
  if (typeof entry === 'string') return entry;
  return entry.name || entry.fullName || entry.person?.fullName || '';
}

const winningPitcher = computed(() => {
  const winner =
    game.value?.summary?.winningPitcher || game.value?.liveData?.decisions?.winner;
  return pitcherName(winner) || '—';
});

const losingPitcher = computed(() => {
  const loser =
    game.value?.summary?.losingPitcher || game.value?.liveData?.decisions?.loser;
  return pitcherName(loser) || '—';
});

const savePitcher = computed(() => {
  const saver =
    game.value?.summary?.savePitcher || game.value?.liveData?.decisions?.save;
  return pitcherName(saver) || '—';
});

const homers = computed(() => {
  const entries = [];
  for (const side of ['away', 'home']) {
    const batters = boxscoreTeams.value[side]?.batters ?? [];
    for (const id of batters) {
      const hr = playerStat(side, id, 'batting', 'homeRuns');
      if (hr && Number(hr) > 0) {
        entries.push(`${playerName(side, id)} (${hr})`);
      }
    }
  }
  return entries.length ? entries.join(', ') : '—';
});

const attendance = computed(() => {
  const att = (boxscore.value?.info || []).find(i => i.label === 'Att')?.value;
  if (!att) return '—';
  return typeof att === 'number' ? att.toLocaleString() : att;
});

const gameDuration = computed(() => {
  const time = (boxscore.value?.info || []).find(i => i.label === 'T')?.value;
  if (!time) return '—';
  return typeof time === 'number' ? time.toLocaleString() : time;
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
  background-color: #f8f8f8;
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
  color: #333;
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
  background-color: #333;
  color: #fff;
}

.linescore th,
.linescore td {
  border: 1px solid #ccc;
  text-align: center;
}

.linescore thead th {
  color: #fff;
}

.linescore tbody th {
  background-color: #e0e0e0;
  color: #333;
}

.linescore td {
  color: #333;
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
  flex: 0 0 100%;
  /* always full width */
  margin: 0 0 1rem;
}

.team-boxscore {
  flex: 0 0 49%;
  /* each takes half width */
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
  background-color: #333;
  color: #fff;
}

.boxscore-table th,
.boxscore-table td {
  border: 1px solid #ccc;
  text-align: center;
}

.boxscore-table th {
  padding: 8px 12px;
  color: #fff;
}

.boxscore-table td {
  padding: 4px 8px;
  color: #333;
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
  color: #333;
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

.summary-info p {
  margin: 8px 0;
}

.summary-info .title {
  font-weight: bold;
}

.top-performers ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.top-performers li {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.top-performers .player-name {
  font-weight: bold;
  margin-right: 0.25rem;
}

.top-performers .team-logo {
  width: 20px;
  height: 20px;
  margin: 0 0.25rem 0 0;
}
</style>
