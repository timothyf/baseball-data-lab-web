import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import { useScheduleStore } from './store/schedule';
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';
import 'primeicons/primeicons.css';
import './global.css';

const scheduleElement = document.getElementById('schedule-data');
const scheduleData = scheduleElement ? JSON.parse(scheduleElement.textContent) : [];

const app = createApp(App);
const pinia = createPinia();
app.use(pinia);
app.use(router);
app.use(PrimeVue, { theme: { preset: Aura } });

const scheduleStore = useScheduleStore(pinia);
scheduleStore.schedule = scheduleData;

app.mount('#vue-app');
