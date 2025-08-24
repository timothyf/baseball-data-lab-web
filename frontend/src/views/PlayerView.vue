<template>
  <section class="player-view">
    <div class="player-container">
      <div class="player-header">
        <img
          v-if="headshotSrc"
          :src="headshotSrc"
          alt="Player headshot"
          class="headshot"
        />
        <div class="player-info">
          <h1>{{ name }}</h1>
          <p v-if="position" class="position">{{ position }}</p>
          <div v-if="teamName" class="team-info">
            <img
              v-if="teamLogoSrc"
              :src="teamLogoSrc"
              alt="Team logo"
              class="team-logo"
            />
            <span>{{ teamName }}</span>
          </div>
        </div>
      </div>

      <div class="player-details">
        <p class="player-id">ID: {{ id }}</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const { id, name } = defineProps({
  id: String,
  name: String
});

const headshotSrc = computed(() => `/api/player/${id}/headshot/`);
const teamName = ref('');
const position = ref('');
const teamLogoSrc = ref('');

onMounted(async () => {
  try {
    const resp = await fetch(`/api/players/${id}/`);
    if (resp.ok) {
      const data = await resp.json();
      teamName.value = data.team_name || '';
      position.value = data.position || '';
      if (data.team_id) {
        try {
          const logoResp = await fetch(`/api/teams/${data.team_id}/logo/`);
          if (logoResp.ok) {
            teamLogoSrc.value = (await logoResp.text()).trim();
          }
        } catch (e) {
          console.error('Failed to fetch team logo', e);
        }
      }
    }
  } catch (e) {
    console.error('Failed to load player info', e);
  }
});
</script>

<style scoped>
.player-view {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  color: #fff;
  padding: 2rem 1rem;
}

.player-container {
  max-width: 800px;
  margin: 0 auto;
}

.player-header {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 1rem;
  text-align: left;
}

.headshot {
  width: 150px;
  height: auto;
  border-radius: 0.5rem;
}

.player-info h1 {
  margin: 0;
  font-size: 2.5rem;
  font-weight: 700;
}

.position {
  margin: 0.25rem 0 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-accent);
}

.team-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.team-logo {
  width: 40px;
  height: 40px;
}

.player-details {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  padding: 1rem;
  margin: 0 auto;
  max-width: 400px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.player-details:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.player-id {
  margin: 0;
}
</style>

