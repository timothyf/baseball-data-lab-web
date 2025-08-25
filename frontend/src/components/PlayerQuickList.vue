<template>
  <div class="player-list">
    <h2>{{ title }}</h2>
    <ul>
      <li v-for="player in players" :key="player.id">
        <RouterLink
          :to="{ name: 'Player', params: { id: player.id }, query: { name: player.name } }"
        >
          {{ player.name }}
        </RouterLink>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  players: {
    type: Array,
    required: true
  }
});
</script>

<style scoped>
.player-list {
  margin-bottom: 2rem;
}
.player-list h2 {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}
.player-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.player-list li {
  margin-bottom: 0.25rem;
}
.player-list a {
  color: var(--color-accent);
}
</style>

