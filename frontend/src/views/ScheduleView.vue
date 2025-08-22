<template>
  <div v-if="scheduleStore.schedule && scheduleStore.schedule.length">
    <DataView :value="allGames" layout="list">
      <template #header>
        <div class="schedule-header">
          <button class="nav-btn" @click="prevDay">&#8592;</button>
          <h2 class="header-date">
            {{ currentDate() === today ? `Today - ${formatDate(currentDate())}` : formatDate(currentDate()) }}
          </h2>
          <button class="nav-btn" @click="nextDay">&#8594;</button>
        </div>
      </template>
      <template #list="slotProps">
        <div class="game-list">
          <GameRow v-for="game in slotProps.items" :key="game.gamePk" :game="game" />
        </div>
      </template>
    </DataView>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useScheduleStore } from '../store/schedule';
import GameRow from '../components/GameRow.vue';

const scheduleStore = useScheduleStore();

const today = new Date().toISOString().slice(0, 10);


const allGames = computed(() =>
  scheduleStore.schedule.flatMap((d) => d.games || [])
);

function currentDate() {
  const dateStr =
    scheduleStore.schedule[0]?.date ||
    scheduleStore.schedule[0]?.games[0]?.gameDate;
  return dateStr ? dateStr.slice(0, 10) : today;
}

async function fetchSchedule(dateStr) {
  const resp = await fetch(`/api/schedule/?date=${dateStr}`);
  scheduleStore.schedule = await resp.json();
}

function adjustDay(delta) {
  const date = new Date(currentDate());
  date.setDate(date.getDate() + delta);
  const iso = date.toISOString().split('T')[0];
  fetchSchedule(iso);
}

function prevDay() {
  adjustDay(-1);
}

function nextDay() {
  adjustDay(1);
}

function formatDate(dateStr) {
  if (!dateStr) return '';
  let date;
  if (/^\d{4}-\d{2}-\d{2}$/.test(dateStr)) {
    try {
      const [y, m, d] = dateStr.split('-').map(Number);
      const noonUTC = Date.UTC(y, m - 1, d, 12, 0, 0);
      const tz = 'America/New_York';
      const hourInNY = Number(
        new Intl.DateTimeFormat('en-US', { timeZone: tz, hour: '2-digit', hour12: false }).format(noonUTC)
      );
      const offset = 12 - hourInNY;
      const offsetStr = String(Math.abs(offset)).padStart(2, '0');
      const sign = offset >= 0 ? '-' : '+';
      date = new Date(`${dateStr}T00:00:00${sign}${offsetStr}:00`);
    } catch {
      date = new Date(`${dateStr}T00:00:00-05:00`);
    }
  } else {
    date = new Date(dateStr);
  }
  return date.toLocaleDateString(undefined, {
    weekday: 'long',
    month: 'short',
    day: 'numeric',
    timeZone: 'America/New_York'
  });
}

</script>

<style scoped>
.schedule-day {
  margin-bottom: 1.5rem;
}

.game-list {
  list-style: none;
  padding: 0;
  margin: 0;
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
}

.nav-btn {
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
}
</style>
