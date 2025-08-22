<template>
  <div>
    <div v-if="game">
      <h2>{{ awayTeam }} @ {{ homeTeam }}</h2>
      <h3 class="game-date">{{ game.gameDate }}</h3>
      <table v-if="innings.length" class="linescore" :style="{ '--team-color': '#f0f0f0' }">
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
      <div v-if="boxscore" class="boxscore">
        <h3>Boxscore</h3>
        <div v-for="side in ['away', 'home']" :key="side" class="team-boxscore">
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

onMounted(async () => {
  const resp = await fetch(`/api/games/${game_pk}/`);
  if (resp.ok) {
    game.value = await resp.json();
  }

  // fetch team names
  const homeTeamId = game.value.team_home_id;
  const awayTeamId = game.value.team_away_id;

  if (homeTeamId) {
    const homeResp = await fetch(`/api/teams/${homeTeamId}/`);
    if (homeResp.ok) {
      const data = await homeResp.json();
      game.value.homeTeamName = data.full_name;
      homeColor.value = data.primary_color || data.color || '#ffffff';
    }
  }

  if (awayTeamId) {
    const awayResp = await fetch(`/api/teams/${awayTeamId}/`);
    if (awayResp.ok) {
      const data = await awayResp.json();
      game.value.awayTeamName = data.full_name;
      awayColor.value = data.primary_color || data.color || '#ffffff';
    }
  }
});

const homeTeam = computed(() => game.value.homeTeamName || '');
const awayTeam = computed(() => game.value.awayTeamName || '');



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
.linescore {
  border-collapse: collapse;
}
.linescore thead {
  background-color: var(--team-color);
}
.linescore th,
.linescore td {
  border: 1px solid #ccc;
  padding: 4px 8px;
  text-align: center;
}
.linescore tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

.boxscore {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  margin-top: 20px;
  width: 1000px;
}

.boxscore h3 {
  flex: 0 0 100%;   /* always full width */
  margin: 0 0 1rem;
}

.team-boxscore {
  flex: 0 0 50%;    /* each takes half width */
  box-sizing: border-box;
  padding: 0.5rem;
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
  padding: 4px 8px;
  text-align: center;
}
.boxscore-table tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

.game-date {
  font-size: 20px;
  color: #555;
  margin-top: -8px;
}
</style>
