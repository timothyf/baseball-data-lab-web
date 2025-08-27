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
.teams-view {
  font-family: var(--font-base);
  min-height: 100vh;
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  color: #fff;
  padding: 2rem 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.teams-container {
  max-width: 1100px;
  margin: 0 auto;
  text-align: center;
}

.team-columns {
  display: flex;
  gap: 2rem;
  justify-content: center;
  margin-top: 2rem;
}

.team-column {
  flex: 1;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  padding: 1rem;
}

.team-column h2 {
  color: var(--color-accent);
}

.team-column ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.team-column li {
  margin: 0.5rem 0;
}
</style>


