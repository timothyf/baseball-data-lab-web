<template>
  <div>
    <h1>{{ name }}</h1>
    <img v-if="teamLogoSrc" :src="teamLogoSrc" alt="Team Logo" />
    <p>ID: {{ id }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const { id, name } = defineProps({
  id: String,
  name: String
});

const teamLogoSrc = computed(() => `/api/teams/${id}/logo/`);
</script>

<style scoped>
img {
  max-width: 200px;
}
</style>
