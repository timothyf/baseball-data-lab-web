<template>
  <div>
    <nav class="top-nav">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/schedule">Schedule</RouterLink>
      <RouterLink to="/standings">Standings</RouterLink>
      <RouterLink to="/teams">Teams</RouterLink>
      <RouterLink to="/players">Players</RouterLink>
      <RouterLink to="/leaders">Leaders</RouterLink>
      <RouterLink to="/developer" class="developer-link">Developer</RouterLink>
    </nav>
    <div class="page-wrapper">
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  name: 'BaseLayout'
};
</script>
