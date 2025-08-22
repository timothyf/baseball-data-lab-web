<template>
  <section class="hero">
    <div class="hero-content">
      <img src="http://localhost:5173/logo.png" alt="Baseball Data Lab logo" class="logo" />
      <h1 class="tagline">Data-Driven Baseball Insights</h1>
      <p class="description">
        Advanced stats, interactive visualizations, and real-time standings—your
        baseball analytics hub.
      </p>
      <p class="welcome-message">
        Welcome! Get started by exploring the schedule, diving into player stats,
        or building your own team.
      </p>
      <div class="cta-buttons">
        <router-link to="/schedule" class="cta-button">View Schedule</router-link>
        <router-link to="/players" class="cta-button">Explore Player Stats</router-link>
        <router-link to="/teams" class="cta-button">Create Your Team</router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
</script>

<style scoped>
.hero {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #1e3a8a, #1e40af);
  color: #fff;
  padding: 2rem;
}

.hero-content {
  max-width: 800px;
}

.logo {
  max-width: 200px;
  margin-bottom: 1.5rem;
}

.tagline {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
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

.cta-buttons {
  margin-top: 2rem;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}

.cta-button {
  background-color: #fbbf24;
  color: #1e3a8a;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  font-weight: 600;
  text-decoration: none;
  transition: background-color 0.3s;
}

.cta-button:hover {
  background-color: #f59e0b;
}
</style>
