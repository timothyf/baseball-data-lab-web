<template>
  <section class="schedule">
    <div
      class="schedule-container"
      v-if="scheduleStore.schedule && scheduleStore.schedule.length"
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
  </section>
</template>

<script setup>
import {
  computed,
  onMounted,
  shallowRef,
  watch,
  defineAsyncComponent
} from 'vue';
import { useScheduleStore } from '../store/schedule';

const GameRow = defineAsyncComponent(() =>
  import('../components/GameRow.vue')
);

const scheduleStore = useScheduleStore();

const scheduleCache = new Map();

let controller;

const today = new Date().toISOString().slice(0, 10);

// Cache of Intl.DateTimeFormat instances by locale
const formatterCache = new Map();
// Cache formatted date results keyed by input date string + locale
const formattedDateCache = new Map();
const TIME_ZONE = 'America/New_York';
const nyHourFormatter = new Intl.DateTimeFormat('en-US', {
  timeZone: TIME_ZONE,
  hour: '2-digit',
  hour12: false
});

const games = shallowRef([]);

watch(
  () => scheduleStore.schedule,
  (schedule) => {
    games.value = schedule.flatMap((d) => d.games || []);
  },
  { immediate: true }
);

const currentDate = computed(() => {
  const dateStr =
    scheduleStore.schedule[0]?.date ||
    scheduleStore.schedule[0]?.games[0]?.gameDate;
  return dateStr ? dateStr.slice(0, 10) : today;
});

const headerDate = computed(() =>
  currentDate.value === today
    ? `Today - ${formatDate(currentDate.value)}`
    : formatDate(currentDate.value)
);

async function fetchSchedule(
  dateStr,
  { cacheOnly = false, prefetch = true } = {},
) {
  if (!cacheOnly) {
    if (controller) controller.abort();
    controller = new AbortController();
  }

  if (scheduleCache.has(dateStr)) {
    const cached = scheduleCache.get(dateStr);
    if (!cacheOnly) scheduleStore.schedule = cached;
    if (prefetch && !cacheOnly) prefetchAdjacent(dateStr);
    return cached;
  }

  const options = {};
  if (!cacheOnly) options.signal = controller.signal;
  const resp = await fetch(`/api/schedule/?date=${dateStr}`, options);
  const data = await resp.json();
  scheduleCache.set(dateStr, data);
  if (!cacheOnly) scheduleStore.schedule = data;
  if (prefetch && !cacheOnly) prefetchAdjacent(dateStr);

  // Fetch win probability predictions for each game in parallel
  // const predictionPromises = [];
  // for (const day of scheduleStore.schedule) {
  //   for (const game of day.games || []) {
  //     const p = fetch(`/api/games/${game.gamePk}/prediction/`)
  //       .then((r) => (r.ok ? r.json() : null))
  //       .then((data) => {
  //         if (data) game.prediction = data;
  //       })
  //       .catch(() => {});
  //     predictionPromises.push(p);
  //   }
  // }
  // await Promise.all(predictionPromises);

  return data;
}

function prefetchAdjacent(dateStr) {
  const date = new Date(dateStr);
  const prev = new Date(date);
  const next = new Date(date);
  prev.setDate(prev.getDate() - 1);
  next.setDate(next.getDate() + 1);
  const prevIso = prev.toISOString().split('T')[0];
  const nextIso = next.toISOString().split('T')[0];
  fetchSchedule(prevIso, { cacheOnly: true, prefetch: false });
  fetchSchedule(nextIso, { cacheOnly: true, prefetch: false });
}

async function prevDay() {
  const date = new Date(currentDate.value);
  date.setDate(date.getDate() - 1);
  const iso = date.toISOString().split('T')[0];
  try {
    await fetchSchedule(iso);
  } catch {}
}

async function nextDay() {
  const date = new Date(currentDate.value);
  date.setDate(date.getDate() + 1);
  const iso = date.toISOString().split('T')[0];
  try {
    await fetchSchedule(iso);
  } catch {}
}

function getFormatter(locale) {
  const loc = locale || undefined;
  if (!formatterCache.has(loc)) {
    formatterCache.set(
      loc,
      new Intl.DateTimeFormat(loc, {
        weekday: 'long',
        month: 'short',
        day: 'numeric',
        timeZone: TIME_ZONE
      })
    );
  }
  return formatterCache.get(loc);
}

function formatDate(dateStr, locale) {
  if (!dateStr) return '';
  const cacheKey = `${dateStr}|${locale || ''}`;
  if (formattedDateCache.has(cacheKey)) return formattedDateCache.get(cacheKey);
  let date;
  if (/^\d{4}-\d{2}-\d{2}$/.test(dateStr)) {
    try {
      const [y, m, d] = dateStr.split('-').map(Number);
      const noonUTC = Date.UTC(y, m - 1, d, 12, 0, 0);
      const hourInNY = Number(nyHourFormatter.format(noonUTC));
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
  const formatted = getFormatter(locale).format(date);
  formattedDateCache.set(cacheKey, formatted);
  return formatted;
}

onMounted(() => {
  if (!scheduleStore.schedule.length) {
    fetchSchedule(today);
  }
});

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
</style>
