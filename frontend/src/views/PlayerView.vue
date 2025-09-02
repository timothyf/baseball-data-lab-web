<template>
  <section class="player-view" :style="teamColorStyle">
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
          <div v-if="teamName" class="team-info">
            <img
              v-if="teamLogoSrc"
              :src="teamLogoSrc"
              alt="Team logo"
              class="team-logo"
            />
            <div class="player-details">
              <span class="position">{{ position }}</span>
              <span class="team-name">{{ teamName }}</span>
              <span class="mlbam-id">
                MLBAM_ID:
                <a
                  :href="mlbPlayerUrl"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {{ id }}
                </a>
              </span>
            </div>
          </div>
        </div>
      </div>

      <TabView>
        <TabPanel header="Overview">
          <section
            v-if="hasBio"
            class="player-details biography"
          >
            <h2>Biography</h2>
            <ul class="bio-list">
              <li v-if="birthDate">
                <strong>Birth Date:</strong> {{ formattedBirthDate }}
              </li>
              <li v-if="birthPlace">
                <strong>Birthplace:</strong> {{ birthPlace }}
              </li>
              <li v-if="height">
                <strong>Height:</strong> {{ height }}
              </li>
              <li v-if="weight">
                <strong>Weight:</strong> {{ weight }} lbs
              </li>
              <li v-if="batSide || throwSide">
                <strong>B/T:</strong>
                {{ batSide || '?' }} / {{ throwSide || '?' }}
              </li>
            </ul>
          </section>
        </TabPanel>
        <TabPanel header="Stats">
          <PlayerStats :id="id" />
        </TabPanel>
        <TabPanel header="Splits">
          <PlayerSplits :id="id" />
        </TabPanel>
        <TabPanel header="Game Log">
          <p>Game Log coming soon.</p>
        </TabPanel>
        <TabPanel header="Charts & Trends">
          <p>Charts & Trends coming soon.</p>
        </TabPanel>
      </TabView>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import PlayerStats from '../components/PlayerStats.vue';
import PlayerSplits from '../components/PlayerSplits.vue';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
import teamColors from '../data/teamColors.json';
import { fetchPlayer, fetchTeamLogo } from '../services/api.js';

const { id } = defineProps({
  id: String
});

const headshotSrc = computed(() => `/api/player/${id}/headshot/`);
const mlbPlayerUrl = computed(() => `https://www.mlb.com/player/${id}`);
const name = ref('');
const teamName = ref('');
const position = ref('');
const teamLogoSrc = ref('');
const birthDate = ref('');
const birthPlace = ref('');
const height = ref('');
const weight = ref('');
const batSide = ref('');
const throwSide = ref('');

const teamColorStyle = computed(() => {
  const colors = teamColors[teamName.value] || [];
  return {
    '--color-primary': colors[0]?.hex || '#1e3a8a',
    '--color-secondary': colors[1]?.hex || '#1e40af',
    '--color-accent': colors[2]?.hex || '#fbbf24'
  };
});

const formattedBirthDate = computed(() => {
  if (!birthDate.value) return '';
  try {
    return new Date(birthDate.value).toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  } catch {
    return birthDate.value;
  }
});

const hasBio = computed(() =>
  birthDate.value ||
  birthPlace.value ||
  height.value ||
  weight.value ||
  batSide.value ||
  throwSide.value
);

onMounted(async () => {
  const data = await fetchPlayer(id);
  if (data) {
    name.value = data.name || '';
    teamName.value = data.team_name || '';
    position.value = data.position || '';
    birthDate.value = data.birth_date || '';
    birthPlace.value = data.birth_place || '';
    height.value = data.height || '';
    weight.value = data.weight || '';
    batSide.value = data.bat_side || '';
    throwSide.value = data.throw_side || '';
    if (data.team_id) {
      const logo = await fetchTeamLogo(data.team_id);
      teamLogoSrc.value = (logo || '').trim();
    }
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
  max-width: 1284px;
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
  margin: 0 !important;
  padding: 1rem;
  max-width: 400px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.player-id {
  margin: 0;
}

.biography {
  text-align: left;
}

.bio-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.bio-list li {
  margin: 0.25rem 0;
}

.bio-list strong {
  font-weight: 600;
}

.player-details {
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  padding: 1rem;
  margin: 0 auto;
  max-width: 400px;
  text-align: left;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.team-name {
  font-weight: 600;
}

.mlbam-id {
  color: #888;
}

.mlbam-id a {
  color: inherit;
}
</style>
