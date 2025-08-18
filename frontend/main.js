import { createApp } from 'vue';
import HelloComponent from './components/HelloComponent.vue';
import ScheduleView from './components/ScheduleView.vue';

const scheduleElement = document.getElementById('schedule-data');
const scheduleData = scheduleElement ? JSON.parse(scheduleElement.textContent) : [];

const app = createApp({
  data() {
    return {
      schedule: scheduleData
    };
  }
});

app.component('hello-component', HelloComponent);
app.component('schedule-view', ScheduleView);
app.mount('#vue-app');
