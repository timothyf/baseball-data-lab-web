import { createRouter, createWebHistory } from 'vue-router';
import BaseLayout from '../layouts/BaseLayout.vue';

const routes = [
  {
    path: '/',
    component: BaseLayout,
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('../views/HomeView.vue')
      },
      {
        path: 'schedule',
        name: 'Schedule',
        component: () => import('../views/ScheduleView.vue')
      },
      {
        path: 'standings',
        name: 'Standings',
        component: () => import('../views/StandingsView.vue')
      },
      {
        path: 'teams',
        name: 'Teams',
        component: () => import('../views/TeamsView.vue')
      },
      {
        path: 'team/:mlbam_team_id',
        name: 'Team',
        component: () => import('../views/TeamView.vue'),
        props: route => ({ mlbam_team_id: route.params.mlbam_team_id, name: route.query.name })
      },
      {
        path: 'game/:game_pk',
        name: 'Game',
        component: () => import('../views/GameView.vue'),
        props: route => ({ game_pk: route.params.game_pk })
      },
      {
        path: 'players',
        name: 'Players',
        component: () => import('../views/PlayersView.vue')
      },
      {
        path: 'leaders',
        name: 'Leaders',
        component: () => import('../views/LeadersView.vue')
      },
      {
        path: 'player/:id',
        name: 'Player',
        component: () => import('../views/PlayerView.vue'),
        props: route => ({ id: route.params.id, name: route.query.name })
      },
      {
        path: 'developer',
        name: 'ApiExplorer',
        component: () => import('../views/ApiExplorerView.vue')
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
