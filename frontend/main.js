import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { scheduleStore } from './store/schedule';

const scheduleElement = document.getElementById('schedule-data');
const scheduleData = scheduleElement ? JSON.parse(scheduleElement.textContent) : [];

scheduleStore.schedule = scheduleData;

const app = createApp(App);
app.use(router);
app.mount('#vue-app');
