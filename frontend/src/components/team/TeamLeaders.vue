<template>
  <div v-if="leaders" class="leader-cards">
    <div v-if="leaders.batting || leaders.pitching" class="leaders-section">
      <div v-if="leaders.batting" class="stats-container">
        <h2>Batting Leaders</h2>
        <ul>
          <li v-for="(data, stat) in leaders.batting" :key="`bat-` + stat">
            {{ stat }}:
            <RouterLink :to="{ name: 'Player', params: { id: data.id }, query: { name: data.name } }">
              {{ data.name }}
            </RouterLink>
            {{ ['AVG', 'SLG', 'OPS'].includes(stat) && data.value != null
              ? parseFloat(data.value).toFixed(3).replace(/^0\./, '.')
              : data.value }}
          </li>
        </ul>
      </div>
      <div v-if="leaders.pitching" class="stats-container">
        <h2>Pitching Leaders</h2>
        <ul>
          <li v-for="(data, stat) in leaders.pitching" :key="`pit-` + stat">
            {{ stat }}:
            <RouterLink :to="{ name: 'Player', params: { id: data.id }, query: { name: data.name } }">
              {{ data.name }}
            </RouterLink>
            {{ stat === 'ERA' && data.value != null
              ? parseFloat(data.value).toFixed(2)
              : data.value }}
          </li>
        </ul>
      </div>
    </div>
  </div>
  <div v-else class="leader-cards">
    <Skeleton v-for="n in 2" :key="n" width="45%" height="10rem" />
  </div>
</template>

<script setup>
import Skeleton from 'primevue/skeleton';

const { leaders } = defineProps({
  leaders: { type: Object, default: null }
});
</script>

<style scoped>
.leader-cards {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-top: 1rem;
}

.stats-container {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  padding: 1rem;
  margin: 0 auto 2rem;
  max-width: 100%;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stats-container:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}
</style>
