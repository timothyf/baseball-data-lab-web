<template>
  <div>
    <h1>{{ name }}</h1>
    <img v-if="headshotSrc" :src="headshotSrc" alt="Player headshot" />
    <p>ID: {{ id }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const { id, name } = defineProps({
  id: String,
  name: String
});

const headshotSrc = computed(() => `/api/players/${id}/headshot/`);
</script>

<style scoped>
img {
  max-width: 200px;
}
</style>
