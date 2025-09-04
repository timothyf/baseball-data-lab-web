import { ref } from 'vue';
import { fetchTeamDetails } from '../services/api.js';

// Shared cache for team abbreviations. Components importing this module will
// reuse the same ref instance, avoiding duplicate network requests.
export const teamAbbrevs = ref({});

/**
 * Fetch and cache abbreviations for the given team IDs.
 *
 * @param {Iterable<number|string>} ids - collection of team IDs to fetch
 * @returns {Promise<Object>} resolved with the updated cache map
 */
export async function fetchTeamAbbrevs(ids) {
  const toFetch = [];
  ids && Array.from(ids).forEach(id => {
    if (!teamAbbrevs.value[id]) toFetch.push(id);
  });
  await Promise.all(
    toFetch.map(async tid => {
      const data = await fetchTeamDetails(tid);
      if (data) {
        teamAbbrevs.value[tid] = data.abbrev || tid;
      }
    })
  );
  return teamAbbrevs.value;
}

export default { teamAbbrevs, fetchTeamAbbrevs };
