import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import ScheduleView from '../views/ScheduleView.vue';
import StandingsView from '../views/StandingsView.vue';
import TeamsView from '../views/TeamsView.vue';
import TeamView from '../views/TeamView.vue';
import PlayersView from '../views/PlayersView.vue';
import PlayerView from '../views/PlayerView.vue';

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
  },
  {
    path: '/team/:id',
    name: 'Team',
    component: TeamView,
    props: route => ({ id: route.params.id, name: route.query.name })
  },
  {
    path: '/players',
    name: 'Players',
    component: PlayersView
  },
  {
    path: '/player/:id',
    name: 'Player',
    component: PlayerView,
    props: route => ({ id: route.params.id, name: route.query.name })
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
