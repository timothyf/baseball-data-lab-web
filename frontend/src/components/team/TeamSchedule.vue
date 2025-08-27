<template>
  <div class="recent-schedule" v-if="recentSchedule">
    <div class="schedule-section">
      <h2>Previous Games</h2>
      <div class="schedule-card">
        <ul>
          <li v-for="game in previousGames" :key="`prev-` + game.gamePk">
            <RouterLink :to="{ name: 'Game', params: { game_pk: game.gamePk } }">
              {{ formatDate(game.gameDate) }} {{ describeGame(game, true) }}
            </RouterLink>
          </li>
        </ul>
      </div>
    </div>
    <div class="schedule-section">
      <h2>Upcoming Games</h2>
      <div class="schedule-card">
        <ul>
          <li v-for="game in nextGames" :key="`next-` + game.gamePk">
            {{ formatDate(game.gameDate) }} {{ describeGame(game, false) }}
          </li>
        </ul>
      </div>
    </div>
  </div>
  <div v-else class="recent-schedule">
    <Skeleton v-for="n in 2" :key="n" class="schedule-card" height="8rem" width="45%" />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import Skeleton from 'primevue/skeleton';

const { recentSchedule, mlbamTeamId } = defineProps({
  recentSchedule: { type: Object, default: null },
  mlbamTeamId: { type: [String, Number], required: true }
});

const previousGames = computed(() => {
  const dates = recentSchedule?.previousGameSchedule?.dates ?? [];
  return dates.flatMap(d => d.games);
});

const nextGames = computed(() => {
  const dates = recentSchedule?.nextGameSchedule?.dates ?? [];
  return dates.flatMap(d => d.games);
});

function formatDate(dateStr) {
  const d = new Date(dateStr);
  return isNaN(d) ? dateStr : d.toLocaleDateString();
}

function describeGame(game, includeScore) {
  const home = game.teams.home;
  const away = game.teams.away;
  const teamIdNum = Number(mlbamTeamId);
  const isHome = home.team.id === teamIdNum;
  const opponent = isHome ? away.team.name : home.team.name;
  const vsAt = isHome ? 'vs' : '@';
  let result = '';
  if (includeScore && home.score != null && away.score != null) {
    const usScore = isHome ? home.score : away.score;
    const oppScore = isHome ? away.score : home.score;
    const outcome = usScore > oppScore ? 'W' : (usScore < oppScore ? 'L' : 'T');
    result = ` ${outcome} ${usScore}-${oppScore}`;
  }
  return `${vsAt} ${opponent}${result}`;
}
</script>

<style scoped>
.recent-schedule {
  display: flex;
  margin: 1rem auto 0;
  justify-content: space-between;
  width: 100%;
  max-width: 700px;
  flex-wrap: wrap;
}

.schedule-section {
  margin: 1rem 0;
  flex: 1 1 45%;
}

.schedule-card {
  background: rgba(255, 255, 255, 0.1);
  padding: 1rem;
  border-radius: 0.5rem;
  margin-top: 1rem;
  text-align: left;
  width: 325px;
}

.schedule-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.schedule-card li {
  margin-bottom: 0.25rem;
}

@media (max-width: 600px) {
  .recent-schedule {
    flex-direction: column;
    align-items: center;
  }

  .schedule-section {
    width: 100%;
  }
}
</style>
