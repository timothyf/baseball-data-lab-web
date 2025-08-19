import { createRouter, createWebHistory } from 'vue-router';
import ScheduleView from '../views/ScheduleView.vue';

const routes = [
  {
    path: '/',
    name: 'Schedule',
    component: ScheduleView
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
