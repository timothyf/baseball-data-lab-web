<template>
  <div>
    <h1>{{ name }}</h1>
    <div v-if="teamName" class="team-info">
      <img
        v-if="teamLogoSrc"
        :src="teamLogoSrc"
        alt="Team logo"
        class="team-logo"
      />
      <span>{{ teamName }}</span>
    </div>
    <p v-if="position">{{ position }}</p>
    <img v-if="headshotSrc" :src="headshotSrc" alt="Player headshot" class="headshot" />
    <p>ID: {{ id }}</p>
  </div>
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
.headshot {
  max-width: 200px;
}
.team-logo {
  width: 40px;
  height: 40px;
  margin-right: 8px;
}
.team-info {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
