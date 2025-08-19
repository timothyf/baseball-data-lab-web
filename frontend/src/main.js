import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { scheduleStore } from './store/schedule';
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';
import 'primeicons/primeicons.css';

const scheduleElement = document.getElementById('schedule-data');
const scheduleData = scheduleElement ? JSON.parse(scheduleElement.textContent) : [];

scheduleStore.schedule = scheduleData;

const app = createApp(App);
app.use(router);
app.use(PrimeVue, { theme: { preset: Aura } });
app.mount('#vue-app');
