import { defineStore } from 'pinia';
import { shallowRef } from 'vue';

export const useScheduleStore = defineStore('schedule', {
  state: () => ({
    schedule: shallowRef([])
  }),
  actions: {
    setSchedule(data) {
      this.schedule.value = data;
    }
  }
});
