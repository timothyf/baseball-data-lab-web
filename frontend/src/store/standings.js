import { defineStore } from 'pinia';

export const useStandingsStore = defineStore('standings', {
  state: () => ({
    standings: []
  })
});
