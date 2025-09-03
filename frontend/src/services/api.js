import httpClient from './httpClient';
import logger from '../utils/logger';

const cache = new Map();

// Schedule specific cache with revalidation support
const scheduleCache = new Map();
export const DEFAULT_SCHEDULE_TTL = 60_000;
let scheduleTTL = DEFAULT_SCHEDULE_TTL;

export function setScheduleCacheOptions({ ttl } = {}) {
  if (typeof ttl === 'number') {
    scheduleTTL = ttl;
  }
}

export function invalidateScheduleCache(date) {
  if (date) {
    scheduleCache.delete(date);
  } else {
    scheduleCache.clear();
  }
}

async function apiFetch(
  url,
  { cacheKey, useCache = true, asText = false, signal } = {},
) {
  if (useCache && cacheKey && cache.has(cacheKey)) {
    return cache.get(cacheKey);
  }
  try {
    const response = await httpClient.get(url, {
      responseType: asText ? 'text' : 'json',
      signal,
    });
    const data = response.data;
    if (useCache && cacheKey) {
      cache.set(cacheKey, data);
    }
    return data;
  } catch (e) {
    logger.error(e);
    return null;
  }
}

export async function fetchSchedule(
  date,
  { force = false, ttl = scheduleTTL, signal } = {},
) {
  const cached = scheduleCache.get(date);
  const now = Date.now();
  if (!force && cached && now - cached.timestamp < ttl) {
    return cached.data;
  }
  try {
    const response = await httpClient.get(`/schedule/?date=${date}`, { signal });
    const data = response.data;
    scheduleCache.set(date, { data, timestamp: now });
    return data;
  } catch (e) {
    logger.error(e);
    return null;
  }
}

export const fetchTeamDetails = (id, opts) =>
  apiFetch(`/teams/${id}/`, { cacheKey: `team:${id}`, ...opts });

export const fetchTeamLogo = (id, opts) =>
  apiFetch(`/teams/${id}/logo/`, {
    cacheKey: `teamLogo:${id}`,
    asText: true,
    ...opts,
  });

export const fetchTeamRecord = (id, opts) =>
  apiFetch(`/teams/${id}/record/`, { cacheKey: `teamRecord:${id}`, ...opts });

export const fetchStandings = (opts) =>
  apiFetch('/standings/', { cacheKey: 'standings', ...opts });

export const fetchTopStat = (opts) =>
  apiFetch('/top-stat', { cacheKey: 'topStat', ...opts });

export const fetchPlayer = (id, opts) =>
  apiFetch(`/players/${id}/`, { cacheKey: `player:${id}`, ...opts });

export const fetchPlayerStats = (id, opts) =>
  apiFetch(`/players/${id}/stats/`, { cacheKey: `playerStats:${id}`, ...opts });

export const fetchPlayerSplits = (id, opts) =>
  apiFetch(`/players/${id}/splits/`, { cacheKey: `playerSplits:${id}`, ...opts });

export const fetchPlayerGameLog = (id, statType, season, opts) =>
  apiFetch(
    `/players/${id}/gamelog/?stat_type=${statType}&season=${season}`,
    { cacheKey: `playerGameLog:${id}:${statType}:${season}`, ...opts },
  );

export const fetchTeamRecentSchedule = (id, opts) =>
  apiFetch(`/teams/${id}/recent_schedule/`, {
    cacheKey: `teamRecentSchedule:${id}`,
    ...opts,
  });

export const fetchTeamRoster = (id, opts) =>
  apiFetch(`/teams/${id}/roster/`, {
    cacheKey: `teamRoster:${id}`,
    ...opts,
  });

export const fetchTeamLeaders = (id, opts) =>
  apiFetch(`/teams/${id}/leaders/`, {
    cacheKey: `teamLeaders:${id}`,
    ...opts,
  });

export const fetchBattingLeaders = (
  season,
  statType,
  sortOrder = 'desc',
  limit = 10,
  offset = 0,
  opts,
) =>
  apiFetch(
    `/unified/get_leaderboard_data/?season=${season}&group=hitting&stat_type=${statType}&limit=${limit}&offset=${offset}&sort_order=${sortOrder}`,
    {
      cacheKey: `battingLeaders:${season}:${statType}:${sortOrder}:${limit}:${offset}`,
      ...opts,
    },
  );

export const fetchPitchingLeaders = (
  season,
  statType,
  sortOrder = 'asc',
  limit = 10,
  offset = 0,
  opts,
) =>
  apiFetch(
    `/unified/get_leaderboard_data/?season=${season}&group=pitching&stat_type=${statType}&limit=${limit}&offset=${offset}&sort_order=${sortOrder}`,
    {
      cacheKey: `pitchingLeaders:${season}:${statType}:${sortOrder}:${limit}:${offset}`,
      ...opts,
    },
  );

export const fetchFieldingLeaders = (
  season,
  statType,
  sortOrder = 'desc',
  limit = 10,
  offset = 0,
  opts,
) =>
  apiFetch(
    `/unified/get_leaderboard_data/?season=${season}&group=fielding&stat_type=${statType}&limit=${limit}&offset=${offset}&sort_order=${sortOrder}`,
    {
      cacheKey: `fieldingLeaders:${season}:${statType}:${sortOrder}:${limit}:${offset}`,
      ...opts,
    },
  );

export default {
  fetchTeamDetails,
  fetchTeamLogo,
  fetchTeamRecord,
  fetchStandings,
  fetchSchedule,
  fetchTopStat,
  fetchPlayer,
  fetchPlayerStats,
  fetchTeamRecentSchedule,
  fetchTeamRoster,
  fetchTeamLeaders,
  fetchBattingLeaders,
  fetchPitchingLeaders,
  fetchFieldingLeaders,
  fetchPlayerSplits,
  fetchPlayerGameLog,
};
