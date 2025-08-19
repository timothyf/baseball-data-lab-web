import { createRouter, createWebHistory } from 'vue-router';
import ScheduleView from '../views/ScheduleView.vue';
import StandingsView from '../views/StandingsView.vue';

const routes = [
  {
    path: '/',
    name: 'Schedule',
    component: ScheduleView
  },
  {
    path: '/standings',
    name: 'Standings',
    component: StandingsView
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
