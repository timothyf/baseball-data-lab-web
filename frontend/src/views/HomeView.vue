<template>
  <section class="hero">
    <div class="hero-content">
      <div class="logo-container">
        <img src="http://localhost:5173/logo.jpg" alt="Baseball Data Lab logo" class="logo" />
        <h1 class="tagline">Data-Driven<br />Baseball Insights</h1>
      </div>

      <div class="feature-cards">
        <router-link
          v-for="feature in features"
          :key="feature.title"
          :to="feature.link"
          class="feature-card"
        >
          <i :class="['pi', feature.icon, 'feature-icon']" />
          <h3 class="feature-title">{{ feature.title }}</h3>
          <p class="feature-description">{{ feature.description }}</p>
        </router-link>
      </div>

      <p class="description">
        Advanced stats, interactive visualizations, and real-time standings—your
        baseball analytics hub.
      </p>

      <div class="top-stat" v-if="topStat">
        <h2>Top Stat of the Day</h2>
        <p>{{ topStat }}</p>
      </div>

      <div class="schedule-preview" v-if="schedulePreview.length">
        <h2>Today's Games</h2>
        <ul>
          <li v-for="(game, idx) in schedulePreview" :key="idx">
            {{ game.teams.away.team.name }} @ {{ game.teams.home.team.name }} -
            {{ formatTime(game.gameDate) }}
          </li>
        </ul>
      </div>

      <div class="standings-preview" v-if="standingsPreview.length">
        <h2>Standings Snapshot</h2>
        <ul>
          <li v-for="team in standingsPreview" :key="team.team.id">
            {{ team.team.name }}: {{ team.wins }}-{{ team.losses }}
          </li>
        </ul>
      </div>

    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { fetchTopStat, fetchSchedule, fetchStandings } from '../services/api.js';

const features = [
  {
    title: 'Schedule',
    icon: 'pi-calendar',
    description: 'See upcoming games and past results.',
    link: '/schedule'
  },
  {
    title: 'Standings',
    icon: 'pi-chart-bar',
    description: 'Track how your favorite teams stack up.',
    link: '/standings'
  },
  {
    title: 'Teams',
    icon: 'pi-users',
    description: 'Browse team rosters and stats.',
    link: '/teams'
  },
  {
    title: 'Players',
    icon: 'pi-user',
    description: 'Dive into detailed player analytics.',
    link: '/players'
  }
];

const topStat = ref('');
const schedulePreview = ref([]);
const standingsPreview = ref([]);

function formatTime(dateStr) {
  const d = new Date(dateStr);
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

onMounted(async () => {
  const statData = await fetchTopStat();
  topStat.value = statData?.stat || 'Shohei Ohtani leads the league with 45 HRs.';

  const today = new Date().toISOString().split('T')[0];
  const [schedData, standingsData] = await Promise.all([
    fetchSchedule(today),
    fetchStandings(),
  ]);
  schedulePreview.value = schedData?.[0]?.games ?? [];
  standingsPreview.value = standingsData?.records?.[0]?.teamRecords ?? [];
});
</script>

<style scoped>
.hero {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  min-height: 100vh;
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  color: #fff;
  padding: 2rem;
}

.hero-content {
  max-width: 800px;
}

.logo {
  max-width: 200px;
  margin-bottom: 0.5rem;
}

.tagline {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.feature-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
  max-width: 800px;
}

.feature-card {
  background: rgba(255, 255, 255, 0.15);
  padding: 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  text-decoration: none;
  color: inherit;
  display: block;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.feature-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: var(--color-accent);
}

.feature-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.feature-description {
  font-size: 0.95rem;
}

.description {
  font-size: 1.25rem;
  max-width: 600px;
  margin: 0 auto;
}

.welcome-message {
  margin-top: 1rem;
  font-size: 1.1rem;
}

.top-stat {
  margin-top: 2rem;
  background: rgba(255, 255, 255, 0.1);
  padding: 1rem;
  border-radius: 0.5rem;
}

.schedule-preview,
.standings-preview {
  margin-top: 2rem;
  background: rgba(255, 255, 255, 0.1);
  padding: 1rem;
  border-radius: 0.5rem;
  text-align: left;
}

.schedule-preview ul,
.standings-preview ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.schedule-preview ul {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.25rem 1rem;
}

.schedule-preview li,
.standings-preview li {
  margin-bottom: 0.25rem;
}

.schedule-preview li {
  margin-bottom: 0;
}

.logo-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-bottom: 1rem;
  justify-content: center;
}

.logo-container .logo {
  margin: 0;
  margin-right: 50px;
}
</style>
