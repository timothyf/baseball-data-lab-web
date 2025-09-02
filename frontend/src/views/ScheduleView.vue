<template>
  <section class="schedule">
    <div
      class="schedule-container"
      v-if="schedule && schedule.length"
    >
      <div class="schedule-header">
        <button class="nav-btn" @click="prevDay">&#8592;</button>
        <h2 class="header-date">{{ headerDate }}</h2>
        <button class="nav-btn" @click="nextDay">&#8594;</button>
      </div>
      <div class="games-list">
        <GameRow
          v-for="game in games"
          :key="game.gamePk"
          :game="game"
        />
      </div>
    </div>
    <Dialog
      v-model:visible="loading"
      modal
      :closable="false"
      :draggable="false"
      :dismissableMask="false"
      :closeOnEscape="false"
      showHeader="false"
      class="loading-dialog"
    >
      <div class="loading-content">
        <ProgressSpinner />
        <p>Loading data...</p>
      </div>
    </Dialog>
  </section>
</template>

<script setup>
import { defineAsyncComponent } from 'vue';
import { useSchedule } from '../composables/useSchedule';
import Dialog from 'primevue/dialog';
import 'primevue/dialog/style';
import ProgressSpinner from 'primevue/progressspinner';
import 'primevue/progressspinner/style';

const GameRow = defineAsyncComponent(() =>
  import('../components/GameRow.vue')
);

const { schedule, games, headerDate, prevDay, nextDay, loading } = useSchedule();
</script>

<style scoped>
.schedule {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  color: #fff;
  padding: 2rem 1rem;
}

.schedule-container {
  max-width: 800px;
  margin: 0 auto;
}

.schedule-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.header-date {
  flex: 1;
  text-align: center;
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.nav-btn {
  background-color: var(--color-accent);
  color: var(--color-primary);
  border: none;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.nav-btn:hover {
  background-color: #f59e0b;
  transform: translateY(-2px);
}

.games-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
}
</style>

