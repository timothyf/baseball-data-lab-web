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
});

const homeTeam = computed(() => game.value?.teams?.home?.team?.name || '');
const awayTeam = computed(() => game.value?.teams?.away?.team?.name || '');
const homeScore = computed(() => game.value?.teams?.home?.score ?? '');
const awayScore = computed(() => game.value?.teams?.away?.score ?? '');
</script>

<style scoped>
</style>
