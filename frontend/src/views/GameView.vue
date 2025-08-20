<template>
  <div>
    <h1>Game {{ game_pk }}</h1>
    <div v-if="game">
      <h2>{{ awayTeam }} @ {{ homeTeam }}</h2>
      <p>Final Score: {{ awayScore }} - {{ homeScore }}</p>
      <table v-if="innings.length" class="linescore">
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
            <th>{{ awayTeam }}</th>
            <td v-for="inning in innings" :key="`away-` + inning.num">{{ inning.away?.runs ?? '' }}</td>
            <td>{{ linescoreTeams.away?.runs ?? '' }}</td>
            <td>{{ linescoreTeams.away?.hits ?? '' }}</td>
            <td>{{ linescoreTeams.away?.errors ?? '' }}</td>
          </tr>
          <tr>
            <th>{{ homeTeam }}</th>
            <td v-for="inning in innings" :key="`home-` + inning.num">{{ inning.home?.runs ?? '' }}</td>
            <td>{{ linescoreTeams.home?.runs ?? '' }}</td>
            <td>{{ linescoreTeams.home?.hits ?? '' }}</td>
            <td>{{ linescoreTeams.home?.errors ?? '' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';

const { game_pk } = defineProps({
  game_pk: { type: [String, Number], required: true }
});

const game = ref(null);

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
      game.value.homeTeamName = (await homeResp.json()).full_name;
    }
  }

  if (awayTeamId) {
    const awayResp = await fetch(`/api/teams/${awayTeamId}/`);
    if (awayResp.ok) {
      game.value.awayTeamName = (await awayResp.json()).full_name;
    }
  }
});

const homeTeam = computed(() => game.value.homeTeamName || '');
const awayTeam = computed(() => game.value.awayTeamName || '');



const homeScore = computed(() => game.value?.teams?.home?.score ?? '');
const awayScore = computed(() => game.value?.teams?.away?.score ?? '');

const innings = computed(() => game.value?.scoreboard?.linescore?.innings ?? []);
const linescoreTeams = computed(() => game.value?.scoreboard?.linescore?.teams ?? {});
</script>

<style scoped>
.linescore {
  border-collapse: collapse;
}
.linescore th,
.linescore td {
  border: 1px solid #ccc;
  padding: 4px 8px;
  text-align: center;
}
</style>
