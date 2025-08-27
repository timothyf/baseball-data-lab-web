<template>
  <section class="teams-view">
    <div class="teams-container">
      <h1>Teams</h1>
      <div class="team-columns">
        <div class="team-column">
          <h2>American League</h2>
          <ul>
            <li
              v-for="team in teams.AL"
              :key="team.mlbam_team_id"
            >
              <RouterLink
                :to="{ name: 'Team', params: { mlbam_team_id: team.mlbam_team_id }, query: { name: team.name } }"
              >
                {{ team.name }}
              </RouterLink>
            </li>
          </ul>
        </div>
        <div class="team-column">
          <h2>National League</h2>
          <ul>
            <li
              v-for="team in teams.NL"
              :key="team.mlbam_team_id"
            >
              <RouterLink
                :to="{ name: 'Team', params: { mlbam_team_id: team.mlbam_team_id }, query: { name: team.name } }"
              >
                {{ team.name }}
              </RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import teams from '../data/mlbTeams.json';
</script>

<style scoped>
.team-columns {
  display: flex;
  gap: 2rem;
}

.team-column {
  flex: 1;
}
</style>


