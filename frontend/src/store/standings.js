import { defineStore } from 'pinia';
import { fetchStandings as apiFetchStandings } from '../services/api.js';

const recordCache = new Map();
let standingsPromise;

export const useStandingsStore = defineStore('standings', {
  state: () => ({
    standings: [],
    standingsByLeague: {
      al: [],
      nl: []
    }
  }),
  actions: {
    async ensureStandings() {
      if (!standingsPromise) {
        standingsPromise = apiFetchStandings()
          .then((data) => {
            this.standings = data || [];
            const grouped = { al: [], nl: [] };
            for (const record of this.standings) {
              const id = String(record.division?.id);
              if (['200', '201', '202'].includes(id)) {
                grouped.al.push(record);
              } else if (['203', '204', '205'].includes(id)) {
                grouped.nl.push(record);
              }
              for (const teamRecord of record?.teamRecords || []) {
                const team = teamRecord?.team;
                if (team?.id != null) {
                  recordCache.set(team.id, {
                    wins: teamRecord.wins,
                    losses: teamRecord.losses,
                  });
                }
              }
            }
            this.standingsByLeague = grouped;
          })
          .catch((e) => {
            console.error(e);
            standingsPromise = null;
          });
      }
      return standingsPromise;
    },
    async fetchTeamRecord(teamId) {
      if (!recordCache.has(teamId)) {
        await this.ensureStandings();
      }
      return recordCache.get(teamId) || null;
    }
  }
});
