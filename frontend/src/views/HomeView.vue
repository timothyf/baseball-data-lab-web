<template>
  <section class="hero">
    <div class="hero-content">
      <img src="http://localhost:5173/logo.jpg" alt="Baseball Data Lab logo" class="logo" />
      <h1 class="tagline">Data-Driven Baseball Insights</h1>

      <div class="feature-cards">
        <div class="feature-card" v-for="feature in features" :key="feature.title">
          <i :class="['pi', feature.icon, 'feature-icon']" />
          <h3 class="feature-title">{{ feature.title }}</h3>
          <p class="feature-description">{{ feature.description }}</p>
        </div>
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

      <div class="cta-buttons">
        <router-link to="/schedule" class="cta-button">View Schedule</router-link>
        <router-link to="/players" class="cta-button">Explore Player Stats</router-link>
        <router-link to="/teams" class="cta-button">Create Your Team</router-link>
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
    description: 'See upcoming games and past results.'
  },
  {
    title: 'Standings',
    icon: 'pi-chart-bar',
    description: 'Track how your favorite teams stack up.'
  },
  {
    title: 'Teams',
    icon: 'pi-users',
    description: 'Browse team rosters and stats.'
  },
  {
    title: 'Players',
    icon: 'pi-user',
    description: 'Dive into detailed player analytics.'
  }
];

const topStat = ref('');

onMounted(async () => {
  try {
    const response = await fetch('/api/top-stat');
    if (response.ok) {
      const data = await response.json();
      topStat.value = data.stat;
      return;
    }
  } catch (e) {
    // Ignore errors and use fallback text
  }
  topStat.value = 'Shohei Ohtani leads the league with 45 HRs.';
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

.cta-buttons {
  margin-top: 2rem;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}

.cta-button {
  background-color: var(--color-accent);
  color: var(--color-primary);
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  font-weight: 600;
  text-decoration: none;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.cta-button:hover {
  background-color: #f59e0b;
  transform: translateY(-2px);
}
</style>
