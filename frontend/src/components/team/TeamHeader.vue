<template>
  <div class="team-header">
    <div class="top-header">
      <img v-if="teamLogoSrc" :src="teamLogoSrc" alt="Team Logo" class="team-logo" />
      <h1 v-if="teamRecord">{{ teamRecord.teamName }}</h1>
    </div>
    <div v-if="teamRecord" class="stats-container">
      <p v-if="teamRecord">
        {{ teamRecord.wins }}-{{ teamRecord.losses }} - {{ formatRank(teamRecord.divisionRank) }}
      </p>
      <table class="team-stats">
        <thead>
          <tr>
            <th>Streak</th>
            <th>Last 10</th>
            <th>Last 30</th>
            <th>RS</th>
            <th>RA</th>
            <th>rDiff</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{{ streakCode }}</td>
            <td>{{ lastTen }}</td>
            <td>{{ lastThirty }}</td>
            <td>{{ runsScored }}</td>
            <td>{{ runsAllowed }}</td>
            <td>{{ runDifferential }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const { teamLogoSrc, teamRecord } = defineProps({
  teamLogoSrc: { type: String, default: '' },
  teamRecord: { type: Object, default: null }
});

function formatRank(rank) {
  if (rank == null) return '';
  const j = rank % 10;
  const k = rank % 100;
  if (j === 1 && k !== 11) return `${rank}st Place`;
  if (j === 2 && k !== 12) return `${rank}nd Place`;
  if (j === 3 && k !== 13) return `${rank}rd Place`;
  return `${rank}th Place`;
}

const streakCode = computed(() => teamRecord?.streak?.streakCode || '');

const lastTen = computed(() => {
  const split = teamRecord?.records?.splitRecords?.find(r => r.type === 'lastTen');
  return split ? `${split.wins}-${split.losses}` : '';
});

const lastThirty = computed(() => {
  const split = teamRecord?.records?.splitRecords?.find(r => r.type === 'lastThirty');
  return split ? `${split.wins}-${split.losses}` : '';
});

const runsScored = computed(() => teamRecord?.runsScored ?? '');
const runsAllowed = computed(() => teamRecord?.runsAllowed ?? '');
const runDifferential = computed(() => teamRecord?.runDifferential ?? '');
</script>

<style scoped>
.team-header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  padding: 3rem;
  font-family: var(--font-base);
  margin: 0 auto;
  max-width: 1100px;
  width: 100%;
  text-align: center;
}

.team-logo {
  max-width: 7.5rem;
  width: 100%;
  height: auto;
}

.stats-container {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  padding: 1rem;
  margin: 0 auto 2rem;
  max-width: 100%;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stats-container:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.team-stats {
  border-collapse: collapse;
  font-family: var(--font-base);
  font-size: 1.6rem;
  width: 100%;
}

.team-stats th,
.team-stats td {
  border: 2px solid var(--color-accent);
  padding: 0.5rem 1rem;
  text-align: center;
}

.team-stats th {
  background-color: var(--color-accent);
  color: var(--color-primary);
  font-weight: 600;
}

.team-header .team-stats th {
  color: white;
}

@media (max-width: 600px) {
  .team-header {
    flex-direction: column;
    padding: 1.5rem 1rem;
  }

  .team-logo {
    margin-right: 0;
    margin-bottom: 1rem;
  }
}
</style>
