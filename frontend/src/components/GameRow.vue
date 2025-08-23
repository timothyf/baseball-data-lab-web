<template>
  <div class="game-row" :style="rowStyle">
    <div class="game-teams">
      <span
        class="team-chip away"
        style="display:inline-flex;align-items:center;padding:2px 6px;margin-right:4px;background:#ffffff;color:var(--color-primary);border-radius:4px;"
      >
        <img
          v-if="game.teams.away.team.logo_url"
          :src="game.teams.away.team.logo_url"
          alt=""
          class="team-logo"
        />
        {{ teamAbbrev(game.teams.away.team) }}
        <span v-if="awayRecord" style="margin-left:4px">{{ awayRecord.wins }}-{{ awayRecord.losses }}</span>
      </span>
      <span style="padding:0 4px;opacity:.6;font-size:1.0rem">@</span>
      <span
        class="team-chip home"
        style="display:inline-flex;align-items:center;padding:2px 6px;margin-left:4px;background:#ffffff;color:var(--color-primary);border-radius:4px;"
      >
        <img
          v-if="game.teams.home.team.logo_url"
          :src="game.teams.home.team.logo_url"
          alt=""
          class="team-logo"
        />
        {{ teamAbbrev(game.teams.home.team) }}
        <span v-if="homeRecord" style="margin-left:4px">{{ homeRecord.wins }}-{{ homeRecord.losses }}</span>
      </span>
    </div>
    <div class="game-time">
      <RouterLink
        v-if="game.status?.detailedState === 'Final'"
        :to="{ name: 'Game', params: { game_pk: game.gamePk } }"
      >
        Final
      </RouterLink>
      <span v-else>{{ gameTime(game) }}</span>
    </div>
    <div class="game-prob" v-if="game.prediction">
      <div class="prob-bar">
        <div class="away" :style="{ width: `${(game.prediction.away * 100).toFixed(0)}%` }"></div>
        <div class="home" :style="{ width: `${(game.prediction.home * 100).toFixed(0)}%` }"></div>
      </div>
      <div class="prob-labels">
        <span>{{ (game.prediction.away * 100).toFixed(0) }}%</span>
        <span>{{ (game.prediction.home * 100).toFixed(0) }}%</span>
      </div>
    </div>
    <div class="game-score" v-if="game.status?.detailedState === 'Final'">
      {{ game.teams.away.score }} - {{ game.teams.home.score }}
    </div>
    <div class="game-broadcasts" v-if="game.broadcasts && game.broadcasts.length">
      {{ game.broadcasts.map(b => b.callSign || b.name).join(', ') }}
    </div>
    <div class="game-pitchers" v-if="game.status?.detailedState === 'Final'">
      <span v-if="game.decisions?.winner" style="padding:4px">
        <strong>W:</strong> {{ shortName(game.decisions.winner.fullName) }}
      </span>
      <span v-if="game.decisions?.loser" style="padding:4px">
        <strong>L:</strong> {{ shortName(game.decisions.loser.fullName) }}
      </span>
      <span v-if="game.decisions?.save" style="padding:4px">
        <strong>S:</strong> {{ shortName(game.decisions.save.fullName) }}
      </span>
    </div>
    <div class="game-pitchers" v-else>
      <span v-if="game.teams.away.probablePitcher">
        {{ shortName(game.teams.away.probablePitcher.fullName) }}
      </span>
      <span v-if="game.teams.home.probablePitcher" style="padding:4px;opacity:.6;">vs</span>
      <span v-if="game.teams.home.probablePitcher">
        {{ shortName(game.teams.home.probablePitcher.fullName) }}
      </span>
    </div>
  </div>
</template>

<script>
const recordCache = new Map();
</script>

<script setup>
import { ref, onMounted } from 'vue';
import { gameTime, teamAbbrev, shortName } from '../composables/gameHelpers';

const { game } = defineProps({
  game: {
    type: Object,
    required: true
  }
});

const homeRecord = ref(null);
const awayRecord = ref(null);

async function fetchTeamRecord(teamId) {
  if (recordCache.has(teamId)) {
    return recordCache.get(teamId);
  }
  try {
    const response = await fetch(`/api/teams/${teamId}/record/`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    const record = { wins: data.wins, losses: data.losses };
    recordCache.set(teamId, record);
    return record;
  } catch (e) {
    console.error(e);
    return null;
  }
}

onMounted(async () => {
  awayRecord.value = await fetchTeamRecord(game.teams.away.team.id);
  homeRecord.value = await fetchTeamRecord(game.teams.home.team.id);
});

const rowStyle = {
  background: 'rgba(255, 255, 255, 0.1)',
  padding: '10px',
  border: '1px solid rgba(255,255,255,0.2)',
  borderRadius: '6px',
  display: 'flex',
  alignItems: 'center',
  gap: '10px',
  fontSize: '.85rem',
  lineHeight: '1.1',
  color: '#000',
  boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
};
</script>

<style scoped>
.game-row {
  display: flex;
  align-items: center;
}

.game-teams {
  width: 250px;
  font-weight: 600;
}

.game-time {
  width: 80px;
}

.game-prob {
  width: 80px;
  font-size: 0.7rem;
  text-align: center;
}

.prob-bar {
  display: flex;
  height: 6px;
  border-radius: 3px;
  overflow: hidden;
  background: #e5e7eb;
  margin-bottom: 2px;
}

.prob-bar .away {
  background: #3b82f6;
}

.prob-bar .home {
  background: #ef4444;
}

.prob-labels {
  display: flex;
  justify-content: space-between;
}

.game-score {
  width: 60px;
  font-weight: 600;
  text-align: center;
}

.game-broadcasts {
  flex: 1;
  font-size: 0.9rem;
  color: rgba(0, 0, 0, 0.8);
}

.game-pitchers {
  width: 270px;
  font-size: 0.9rem;
  color: rgba(0, 0, 0, 0.8);
  text-align: right;
}

.team-logo {
  width: 20px;
  height: 20px;
  margin-right: 4px;
}
</style>

