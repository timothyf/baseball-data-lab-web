<template>
  <section class="hero">
    <div class="hero-content">
      <img src="http://localhost:5173/logo.jpg" alt="Baseball Data Lab logo" class="logo" />
      <h1 class="tagline">Data-Driven Baseball Insights</h1>

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
      <p class="welcome-message">
        Welcome! Get started by exploring the schedule, diving into player stats,
        or building your own team.
      </p>

      <div class="top-stat" v-if="topStat">
        <h2>Top Stat of the Day</h2>
        <p>{{ topStat }}</p>
      </div>

      <div class="news" v-if="newsItems.length">
        <h2>Latest News</h2>
        <ul>
          <li v-for="(item, idx) in newsItems" :key="idx">
            <a :href="item.url" target="_blank" rel="noopener">{{ item.title }}</a>
          </li>
        </ul>
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
const newsItems = ref([]);
const schedulePreview = ref([]);
const standingsPreview = ref([]);

function formatTime(dateStr) {
  const d = new Date(dateStr);
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

onMounted(async () => {
  try {
    const response = await fetch('/api/top-stat');
    if (response.ok) {
      const data = await response.json();
      topStat.value = data.stat;
    }
  } catch (e) {
    // Ignore errors
  }
  if (!topStat.value) {
    topStat.value = 'Shohei Ohtani leads the league with 45 HRs.';
  }

  const today = new Date().toISOString().split('T')[0];
  try {
    const [newsRes, scheduleRes, standingsRes] = await Promise.all([
      fetch('/api/news/'),
      fetch(`/api/schedule/?date=${today}`),
      fetch('/api/standings/'),
    ]);

    if (newsRes.ok) {
      newsItems.value = await newsRes.json();
    }
    if (scheduleRes.ok) {
      const sched = await scheduleRes.json();
      schedulePreview.value = sched[0]?.games?.slice(0, 5) ?? [];
    }
    if (standingsRes.ok) {
      const standings = await standingsRes.json();
      standingsPreview.value =
        standings.records?.[0]?.teamRecords?.slice(0, 5) ?? [];
    }
  } catch (e) {
    // Ignore errors for dynamic content
  }
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

.news,
.schedule-preview,
.standings-preview {
  margin-top: 2rem;
  background: rgba(255, 255, 255, 0.1);
  padding: 1rem;
  border-radius: 0.5rem;
  text-align: left;
}

.news ul,
.schedule-preview ul,
.standings-preview ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.news li,
.schedule-preview li,
.standings-preview li {
  margin-bottom: 0.25rem;
}
</style>
