import { defineStore } from 'pinia';

export const useTeamsStore = defineStore('teams', {
  state: () => ({
    teams: [],
    details: {},
    rosters: {},
    standings: {},
    leaders: {}
  }),
  getters: {
    getDetails: (state) => (id) => state.details[id],
    getRoster: (state) => (id) => state.rosters[id],
    getStandings: (state) => (id) => state.standings[id],
    getLeaders: (state) => (id) => state.leaders[id]
  },
  actions: {
    setDetails(id, data) {
      this.details[id] = data;
    },
    setRoster(id, data) {
      this.rosters[id] = data;
    },
    setStandings(id, data) {
      this.standings[id] = data;
    },
    setLeaders(id, data) {
      this.leaders[id] = data;
    }
  }
});
