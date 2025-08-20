<template>
  <div>
    <h1>Game {{ game_pk }}</h1>
    <div v-if="game">
      <h2>{{ awayTeam }} @ {{ homeTeam }}</h2>
      <p>Final Score: {{ awayScore }} - {{ homeScore }}</p>
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
</script>

<style scoped>
</style>
