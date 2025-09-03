import {
  computed,
  onMounted,
  onBeforeUnmount,
  onScopeDispose,
  ref,
  shallowRef,
  watch,
} from 'vue';
import { storeToRefs } from 'pinia';
import { useScheduleStore } from '../store/schedule';
import {
  fetchSchedule as apiFetchSchedule,
  DEFAULT_SCHEDULE_TTL,
} from '../services/api';
import logger from '../utils/logger';

const REVALIDATE_INTERVAL = DEFAULT_SCHEDULE_TTL;

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

let controller;
let refreshInterval;

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

export function useSchedule() {
  const scheduleStore = useScheduleStore();
  const { schedule } = storeToRefs(scheduleStore);

  const today = new Date().toISOString().slice(0, 10);

  const games = shallowRef([]);
  const loading = ref(false);

  watch(
    schedule,
    (scheduleVal) => {
      games.value = Array.isArray(scheduleVal)
        ? scheduleVal.flatMap((d) => d?.games || [])
        : [];
    },
    { immediate: true }
  );

  const currentDate = computed(() => {
    const scheduleVal = schedule.value;
    const dateStr =
      scheduleVal[0]?.date ||
      // Use optional chaining for array access to avoid errors when the
      // schedule array is empty.
      scheduleVal[0]?.games?.[0]?.gameDate;
    return dateStr ? dateStr.slice(0, 10) : today;
  });

  const headerDate = computed(() =>
    currentDate.value === today
      ? `Today - ${formatDate(currentDate.value)}`
      : formatDate(currentDate.value)
  );

  async function fetchSchedule(
    dateStr,
    { cacheOnly = false, prefetch = true, force = false } = {},
  ) {
    if (!cacheOnly) {
      if (controller) controller.abort();
      controller = new AbortController();
      loading.value = true;
    }

    try {
      const data = await apiFetchSchedule(dateStr, {
        force,
        ttl: REVALIDATE_INTERVAL,
        signal: cacheOnly ? undefined : controller.signal,
      });
      if (!cacheOnly && data) {
        scheduleStore.setSchedule(data);
        if (prefetch) prefetchAdjacent(dateStr);
      }
      return data;
    } finally {
      if (!cacheOnly) loading.value = false;
    }
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
      await fetchSchedule(iso, { force: iso === today });
    } catch (e) {
      logger.error(e);
    }
  }

  async function nextDay() {
    const date = new Date(currentDate.value);
    date.setDate(date.getDate() + 1);
    const iso = date.toISOString().split('T')[0];
    try {
      await fetchSchedule(iso, { force: iso === today });
    } catch (e) {
      logger.error(e);
    }
  }

  watch(
    currentDate,
    (newDate) => {
      if (refreshInterval) {
        clearInterval(refreshInterval);
        refreshInterval = null;
      }
      if (newDate === today) {
        refreshInterval = setInterval(() => {
          fetchSchedule(today, { force: true });
        }, REVALIDATE_INTERVAL);
      }
    },
    { immediate: true }
  );

  onMounted(() => {
    fetchSchedule(today, { force: true });
  });

  function clearRefreshInterval() {
    if (refreshInterval) {
      clearInterval(refreshInterval);
      refreshInterval = null;
    }
  }

  onBeforeUnmount(clearRefreshInterval);
  onScopeDispose(clearRefreshInterval);

  return { schedule, games, headerDate, prevDay, nextDay, loading, fetchSchedule };
}

export { formatDate };

