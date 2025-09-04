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
              <li v-if="fullName">
                <strong>{{ fullName }}</strong>
              </li>
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
              <li v-if="formattedDraft">
                <strong>Draft:</strong> {{ formattedDraft }}
              </li>
              <li v-if="schoolInfo">
                <strong>School:</strong> {{ schoolInfo }}
              </li>
              <li v-if="mlbDebutDate">
                <strong>MLB Debut:</strong> {{ mlbDebutDate }}
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
          <PlayerGameLog v-if="position" :id="id" :stat-type="statType" />
        </TabPanel>
        <TabPanel header="Charts & Trends">
          <p>Charts & Trends coming soon.</p>
        </TabPanel>
      </TabView>
    </div>
    <LoadingDialog :visible="loading" />
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import PlayerStats from '../components/PlayerStats.vue';
import PlayerSplits from '../components/PlayerSplits.vue';
import PlayerGameLog from '../components/PlayerGameLog.vue';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
import LoadingDialog from '../components/LoadingDialog.vue';
import { useTeamColors } from '../composables/useTeamColors.js';
import { fetchPlayer } from '../services/api.js';

const { id } = defineProps({
  id: String
});

const headshotSrc = computed(() => `/api/player/${id}/headshot/`);
const mlbPlayerUrl = computed(() => `https://www.mlb.com/player/${id}`);
const name = ref('');
const teamName = ref('');
const position = ref('');
const birthDate = ref('');
const birthPlace = ref('');
const fullName = ref('');
const height = ref('');
const weight = ref('');
const batSide = ref('');
const throwSide = ref('');
const draft = ref(null);
const mlbDebutDate = ref('');
const loading = ref(true);

const statType = computed(() => (position.value === 'Pitcher' ? 'pitching' : 'hitting'));

const teamColorStyle = useTeamColors(teamName);

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

const formattedDraft = computed(() => {
  const d = draft.value;
  if (!d) return '';
  const parts = [];
  if (d.year) parts.push(d.year);
  if (d.team_name) parts.push(d.team_name);
  const roundPick = [];
  if (d.round) roundPick.push(`Round ${d.round}`);
  if (d.pick) roundPick.push(`Pick ${d.pick}`);
  if (roundPick.length) parts.push(roundPick.join(', '));
  if (d.overall) parts.push(`Overall Pick ${d.overall}`);
  return parts.join(' - ');
});

const schoolInfo = computed(() => {
  const d = draft.value;
  if (!d) return '';
  const parts = [];
  if (d.school) parts.push(`${d.school.name}, ${d.school.state}, ${d.school.country}`);
  return parts.join(' - ');
});

const hasBio = computed(() =>
  birthDate.value ||
  birthPlace.value ||
  fullName.value ||
  mlbDebutDate.value ||
  height.value ||
  weight.value ||
  batSide.value ||
  throwSide.value ||
  formattedDraft.value
);

onMounted(async () => {
  try {
    const data = await fetchPlayer(id);
    if (data) {
      name.value = data.name || '';
      teamName.value = data.team_name || '';
      position.value = data.position || '';
      birthDate.value = data.birth_date || '';
      birthPlace.value = data.birth_place || '';
      fullName.value = data.full_name || '';
      mlbDebutDate.value = data.mlb_debut_date || '';
      height.value = data.height || '';
      weight.value = data.weight || '';
      batSide.value = data.bat_side || '';
      throwSide.value = data.throw_side || '';
      draft.value = data.draft || null;
    }
  } finally {
    loading.value = false;
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
