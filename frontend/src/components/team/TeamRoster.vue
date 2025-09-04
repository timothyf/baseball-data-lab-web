<template>
  <div v-if="batters.length || pitchers.length" class="roster-section">
    <div v-if="batters.length" class="stats-container roster">
      <h2>Batters ({{ batters.length }})</h2>
      <table class="team-stats roster-table">
        <thead class="roster-head">
          <tr>
            <th>Name</th>
            <th>Age</th>
            <th>Pos</th>
            <th>Bats</th>
            <th>#</th>
            <th>MLB ID</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="group in battersByPosition" :key="group.position">
            <tr class="position-row">
              <th colspan="6">{{ group.position }}</th>
            </tr>
            <tr v-for="player in group.players" :key="player.person.id">
              <td>
                <RouterLink :to="{ name: 'Player', params: { id: player.person.id } }">
                  {{ player.person.fullName }}
                </RouterLink>
              </td>
              <td>{{ player.person?.currentAge ?? '' }}</td>
              <td>{{ player.position.abbreviation }}</td>
              <td>{{ player.person?.batSide?.code ?? '' }}</td>
              <td>{{ player.person?.primaryNumber ?? '' }}</td>
              <td>
                <a :href="`https://www.mlb.com/player/${player.person.id}`" target="_blank" rel="noopener noreferrer">
                  {{ player.person.id ?? '' }}
                </a>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
    <div v-if="pitchers.length" class="stats-container roster">
      <h2>Pitchers ({{ pitchers.length }})</h2>
      <table class="team-stats roster-table">
        <thead class="roster-head">
          <tr>
            <th>Name</th>
            <th>Age</th>
            <th>Throws</th>
            <th>#</th>
            <th>MLB ID</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="player in pitchers" :key="player.person.id">
            <td>
              <RouterLink :to="{ name: 'Player', params: { id: player.person.id } }">
                {{ player.person.fullName }}
              </RouterLink>
            </td>
            <td>{{ player.person?.currentAge ?? '' }}</td>
            <td>{{ player.person?.pitchHand?.code ?? '' }}</td>
            <td>{{ player.person?.primaryNumber ?? '' }}</td>
            <td>
              <a :href="`https://www.mlb.com/player/${player.person.id}`" target="_blank" rel="noopener noreferrer">
                {{ player.person.id ?? '' }}
              </a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <div v-else class="roster-section">
    <Skeleton v-for="n in 2" :key="n" class="stats-container roster" height="15rem" />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import Skeleton from 'primevue/skeleton';

const { roster } = defineProps({
  roster: { type: Array, default: () => [] }
});

const batters = computed(() =>
  roster.filter(p => p.position?.abbreviation !== 'P')
);

const pitchers = computed(() =>
  roster.filter(p => p.position?.abbreviation === 'P')
);

const battersByPosition = computed(() => {
  const order = ['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'OF', 'DH'];
  const groups = batters.value.reduce((acc, player) => {
    const pos = player.position?.abbreviation || 'Other';
    if (!acc[pos]) acc[pos] = [];
    acc[pos].push(player);
    return acc;
  }, {});
  return Object.keys(groups)
    .sort((a, b) => {
      const ai = order.indexOf(a);
      const bi = order.indexOf(b);
      if (ai === -1 && bi === -1) return a.localeCompare(b);
      if (ai === -1) return 1;
      if (bi === -1) return -1;
      return ai - bi;
    })
    .map(pos => ({
      position: pos,
      players: groups[pos].sort((a, b) =>
        (a.person?.fullName ?? '').localeCompare(b.person?.fullName ?? '')
      ),
    }));
});
</script>

<style scoped>
.roster-section {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.roster {
  flex: 1 1 45%;
  margin: 0 auto 1rem;
  padding: 0.5rem;
}

.roster-table {
  font-size: 1.2rem;
}

.roster-table th,
.roster-table td {
  padding: 0.25rem 0.5rem;
}

.position-row th {
  background-color: var(--color-secondary);
  color: #fff;
  text-align: left;
}

.roster-head tr th {
  color: white;
}
</style>
