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
        <span class="field-value" v-if="player.value != null"> {{ formatValue(player.value) }}</span>
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
  },
  decimalPlaces: {
    type: Number,
    default: null,
  },
});

const formatValue = (val) => {
  const num = Number(val);
  if (!isNaN(num)) {
    if (props.decimalPlaces !== null) {
      return num.toFixed(props.decimalPlaces);
    }
    if (num < 1) {
      return num.toFixed(3).replace(/^0\./, '.');
    }
    return num.toString();
  }
  return val;
};
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

.field-value {
  margin-left: 0.5rem;
}
</style>

