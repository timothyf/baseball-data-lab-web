import { defineStore } from 'pinia';
import { shallowRef } from 'vue';

// Using the setup-style store ensures the `schedule` remains a ref. When
// `shallowRef` was used directly in the state of an options store, Pinia
// unwrapped it, causing it to lose its ref behavior. Components that watched
// the schedule then received a plain array and Vue reported "Invalid watch
// source" errors. Exposing a ref from the setup store keeps it reactive and
// avoids those errors.
export const useScheduleStore = defineStore('schedule', () => {
  const schedule = shallowRef([]);

  function setSchedule(data) {
    schedule.value = data;
  }

  return { schedule, setSchedule };
});
