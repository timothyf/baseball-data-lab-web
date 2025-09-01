const cache = new Map();

async function apiFetch(url, { cacheKey, useCache = true, asText = false } = {}) {
  if (useCache && cacheKey && cache.has(cacheKey)) {
    return cache.get(cacheKey);
  }
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = asText ? await res.text() : await res.json();
    if (useCache && cacheKey) {
      cache.set(cacheKey, data);
    }
    return data;
  } catch (e) {
    console.error('API fetch failed for', url, e);
    return null;
  }
}

export const fetchTeamDetails = (id, opts) =>
  apiFetch(`/api/teams/${id}/`, { cacheKey: `team:${id}`, ...opts });

export const fetchTeamLogo = (id, opts) =>
  apiFetch(`/api/teams/${id}/logo/`, {
    cacheKey: `teamLogo:${id}`,
    asText: true,
    ...opts,
  });

export const fetchTeamRecord = (id, opts) =>
  apiFetch(`/api/teams/${id}/record/`, { cacheKey: `teamRecord:${id}`, ...opts });

export const fetchStandings = (opts) =>
  apiFetch('/api/standings/', { cacheKey: 'standings', ...opts });

export const fetchSchedule = (date, opts) =>
  apiFetch(`/api/schedule/?date=${date}`, { cacheKey: `schedule:${date}`, ...opts });

export const fetchTopStat = (opts) =>
  apiFetch('/api/top-stat', { cacheKey: 'topStat', ...opts });

export const fetchPlayer = (id, opts) =>
  apiFetch(`/api/players/${id}/`, { cacheKey: `player:${id}`, ...opts });

export const fetchPlayerStats = (id, opts) =>
  apiFetch(`/api/players/${id}/stats/`, { cacheKey: `playerStats:${id}`, ...opts });

export const fetchTeamRecentSchedule = (id, opts) =>
  apiFetch(`/api/teams/${id}/recent_schedule/`, {
    cacheKey: `teamRecentSchedule:${id}`,
    ...opts,
  });

export const fetchTeamRoster = (id, opts) =>
  apiFetch(`/api/teams/${id}/roster/`, {
    cacheKey: `teamRoster:${id}`,
    ...opts,
  });

export const fetchTeamLeaders = (id, opts) =>
  apiFetch(`/api/teams/${id}/leaders/`, {
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
    `/api/unified/get_leaderboard_data/?season=${season}&group=hitting&stat_type=${statType}&limit=${limit}&offset=${offset}&sort_order=${sortOrder}`,
    {
      cacheKey: `battingLeaders:${season}:${statType}:${sortOrder}:${limit}:${offset}`,
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
};

