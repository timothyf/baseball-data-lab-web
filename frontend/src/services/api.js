import httpClient from './httpClient';
import logger from '../utils/logger';

const cache = new Map();
const PERSIST_PREFIX = 'apiCache:';
export const DEFAULT_PERSIST_TTL = 24 * 60 * 60 * 1000; // 24 hours

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
  {
    cacheKey,
    useCache = true,
    asText = false,
    signal,
    persist = false,
    persistTTL = DEFAULT_PERSIST_TTL,
  } = {},
) {
  const storageKey = cacheKey ? `${PERSIST_PREFIX}${cacheKey}` : null;
  if (useCache && cacheKey) {
    if (cache.has(cacheKey)) {
      return cache.get(cacheKey);
    }
    if (persist && storageKey && typeof localStorage !== 'undefined') {
      try {
        const raw = localStorage.getItem(storageKey);
        if (raw) {
          const { data, timestamp } = JSON.parse(raw);
          if (Date.now() - timestamp < persistTTL) {
            cache.set(cacheKey, data);
            return data;
          }
        }
      } catch (err) {
        logger.error(err);
      }
    }
  }
  try {
    const response = await httpClient.get(url, {
      responseType: asText ? 'text' : 'json',
      signal,
    });
    const data = response.data;
    if (useCache && cacheKey) {
      cache.set(cacheKey, data);
      if (persist && storageKey && typeof localStorage !== 'undefined') {
        try {
          localStorage.setItem(storageKey, JSON.stringify({ data, timestamp: Date.now() }));
        } catch (err) {
          logger.error(err);
        }
      }
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

export const fetchCareerStatsForPlayers = (ids = [], opts) => {
  const param = Array.isArray(ids) ? ids.join(',') : ids;
  return apiFetch(
    `/players/career_stats/?player_ids=${param}`,
    { cacheKey: `playerCareerStats:${param}`, ...opts },
  );
};

export const fetchPlayerSplits = (id, opts) =>
  apiFetch(`/players/${id}/splits/`, { cacheKey: `playerSplits:${id}`, ...opts });

export const fetchPlayerGameLog = (id, statType, season, opts) =>
  apiFetch(
    `/players/${id}/gamelog/?stat_type=${statType}&season=${season}`,
    { cacheKey: `playerGameLog:${id}:${statType}:${season}`, ...opts },
  );

export const fetchPlayerStatcastBatterData = (id, startDate, endDate, opts) =>
  apiFetch(
    `/players/${id}/statcast/batter/?start_date=${startDate}&end_date=${endDate}`,
    { cacheKey: `playerStatcastBatter:${id}:${startDate}:${endDate}`, ...opts },
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

export const fetchLeaders = ({
  group,
  season,
  league_ids,
  team_id,
  statType,
  sortOrder = 'desc',
  limit = 10,
  offset = 0,
  ...opts
} = {}) => {
  const leagueIdsValue = Array.isArray(league_ids)
    ? league_ids.join(',')
    : league_ids || '103,104';

  const params = new URLSearchParams({
    season,
    league_ids: leagueIdsValue,
    team_id,
    group,
    stat_type: statType,
    limit,
    offset,
    sort_order: sortOrder,
  });

  return apiFetch(
    `/unified/fetch_leaderboard_data/?${params.toString()}`,
    {
      cacheKey: `leaders:${group}:${season}:${leagueIdsValue}:${team_id}:${statType}:${sortOrder}:${limit}:${offset}`,
      ...opts,
    },
  );
};

export const fetchBattingLeaders = ({ sortOrder = 'desc', ...params } = {}) =>
  fetchLeaders({ group: 'hitting', sortOrder, ...params });

export const fetchPitchingLeaders = ({ sortOrder = 'asc', ...params } = {}) =>
  fetchLeaders({ group: 'pitching', sortOrder, ...params });

export const fetchFieldingLeaders = ({ sortOrder = 'desc', ...params } = {}) =>
  fetchLeaders({ group: 'fielding', sortOrder, ...params });

export const fetchHallOfFamePlayers = (opts) =>
  apiFetch('/players/halloffame/', {
    cacheKey: 'hallOfFame',
    persist: true,
    persistTTL: DEFAULT_PERSIST_TTL,
    ...opts,
  });

export default {
  fetchTeamDetails,
  fetchTeamLogo,
  fetchTeamRecord,
  fetchStandings,
  fetchSchedule,
  fetchTopStat,
  fetchPlayer,
  fetchPlayerStats,
  fetchCareerStatsForPlayers,
  fetchTeamRecentSchedule,
  fetchTeamRoster,
  fetchTeamLeaders,
  fetchLeaders,
  fetchBattingLeaders,
  fetchPitchingLeaders,
  fetchFieldingLeaders,
  fetchHallOfFamePlayers,
  fetchPlayerSplits,
  fetchPlayerGameLog,
  fetchPlayerStatcastBatterData,
};
