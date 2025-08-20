import { defineStore } from 'pinia';

export const useTeamsStore = defineStore('teams', {
  state: () => ({
    teams: []
  })
});
