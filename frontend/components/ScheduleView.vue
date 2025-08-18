<template>
  <div v-if="schedule && schedule.length">
    <h2>Today's Schedule</h2>
    <ul>
      <li v-for="(day, dIndex) in schedule" :key="dIndex">
        <ul>
          <li v-for="game in day.games" :key="game.gamePk">
            {{ game.teams.away.team.name }} at {{ game.teams.home.team.name }} - {{ game.gameDate }}
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'ScheduleView',
  props: {
    schedule: {
      type: Array,
      default: () => []
    }
  }
};
</script>
