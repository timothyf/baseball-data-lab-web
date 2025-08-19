import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import ScheduleView from '../views/ScheduleView.vue';
import StandingsView from '../views/StandingsView.vue';
import TeamsView from '../views/TeamsView.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/schedule',
    name: 'Schedule',
    component: ScheduleView
  },
  {
    path: '/standings',
    name: 'Standings',
    component: StandingsView
  },
  {
    path: '/teams',
    name: 'Teams',
    component: TeamsView
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
