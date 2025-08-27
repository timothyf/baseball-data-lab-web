<template>
  <div>
    <nav class="top-nav">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/schedule">Schedule</RouterLink>
      <RouterLink to="/standings">Standings</RouterLink>
      <RouterLink to="/teams">Teams</RouterLink>
      <RouterLink to="/players">Players</RouterLink>
      <RouterLink to="/developer" class="developer-link">Developer</RouterLink>
    </nav>
    <router-view />
  </div>
</template>

<script>

export default {
  name: 'App',
  components: {
  }
};
</script>

