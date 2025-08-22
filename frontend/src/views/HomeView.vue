<template>
  <section class="hero">
    <div class="hero-content">
      <img src="http://localhost:5173/logo.png" alt="Baseball Data Lab logo" class="logo" />
      <h1 class="tagline">Data-Driven Baseball Insights</h1>
      <p class="description">
        Advanced stats, interactive visualizations, and real-time standings—your
        baseball analytics hub.
      </p>
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
</style>
