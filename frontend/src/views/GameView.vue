<template>
  <div>
    <h1>Game {{ game_pk }}</h1>
  </div>
</template>

<script setup>
const { game_pk } = defineProps({
  game_pk: { type: [String, Number], required: true }
});
</script>

<style scoped>
</style>
