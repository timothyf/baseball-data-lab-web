<template>
  <div>
    <h1>Player</h1>
    <p>ID: {{ id }}</p>
    <p>Name: {{ name }}</p>
  </div>
</template>

<script setup>
const { id, name } = defineProps({
  id: String,
  name: String
});
</script>

<style scoped>
</style>
