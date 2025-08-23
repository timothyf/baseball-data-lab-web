import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import { useScheduleStore } from './store/schedule';

// import PrimeVue from 'primevue/config';
// import Aura from '@primevue/themes/aura';   // brings in both tokens + CSS
// import 'primeicons/primeicons.css';

import './global.css';

import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';
import 'primeicons/primeicons.css';
import 'primevue/dataview/style';
import 'primevue/datatable/style';
import 'primevue/column/style';


const scheduleElement = document.getElementById('schedule-data');
const scheduleData = scheduleElement ? JSON.parse(scheduleElement.textContent) : [];

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

app.use(PrimeVue, {
    // Default theme configuration
    theme: {
        preset: Aura,
        // options: {
        //     prefix: 'p',
        //     darkModeSelector: 'system',
        //     cssLayer: false
        // }
    }
 });

const scheduleStore = useScheduleStore(pinia);
scheduleStore.schedule = scheduleData;

app.mount('#vue-app');

function updateActiveNav(path) {
  const links = document.querySelectorAll('.top-nav a');
  const normalizedPath = path.replace(/\/$/, '');
  links.forEach((link) => {
    const href = link.getAttribute('href').replace(/\/$/, '');
    if (href === normalizedPath) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}

updateActiveNav(router.currentRoute.value.path);
router.afterEach((to) => updateActiveNav(to.path));
