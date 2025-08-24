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
        <span v-if="awayRecord" style="margin-left:4px;color:#888;">{{ awayRecord.wins }}-{{ awayRecord.losses }}</span>
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
        <span v-if="homeRecord" style="margin-left:4px;color:#888;">{{ homeRecord.wins }}-{{ homeRecord.losses }}</span>
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
    <!-- <div class="game-prob" v-if="game.prediction">
      <div class="prob-bar">
        <div class="away" :style="{ width: `${(game.prediction.away * 100).toFixed(0)}%` }"></div>
        <div class="home" :style="{ width: `${(game.prediction.home * 100).toFixed(0)}%` }"></div>
      </div>
      <div class="prob-labels">
        <span>{{ (game.prediction.away * 100).toFixed(0) }}%</span>
        <span>{{ (game.prediction.home * 100).toFixed(0) }}%</span>
      </div>
    </div> -->
    <div class="game-score" v-if="game.status?.detailedState === 'Final'">
      {{ game.teams.away.score }} - {{ game.teams.home.score }}
    </div>
    <div class="game-broadcasts" v-if="game.broadcasts && game.broadcasts.length">
      {{ game.broadcasts.map(b => b.callSign || b.name).join(', ') }}
    </div>
    <div class="game-pitchers" v-if="game.status?.detailedState === 'Final'">
      <span v-if="game.decisions?.winner" style="padding:4px">
        <strong>W:</strong>
                <RouterLink
                  :to="{
                    name: 'Player',
                    params: { id: game.decisions.winner.id },
                    query: { name: game.decisions.winner.fullName }
                  }"
                >
                 {{ shortName(game.decisions.winner.fullName) }}
                </RouterLink>
      </span>
      <span v-if="game.decisions?.loser" style="padding:4px">
        <strong>L:</strong>
        <RouterLink :to="playerLink(game.decisions.loser)">
          {{ shortName(game.decisions.loser.fullName) }}
        </RouterLink>
      </span>
      <span v-if="game.decisions?.save" style="padding:4px">
        <strong>S:</strong>
        <RouterLink :to="playerLink(game.decisions.save)">
          {{ shortName(game.decisions.save.fullName) }}
        </RouterLink>
      </span>
    </div>
    <div class="game-pitchers" v-else>
      <RouterLink
        v-if="game.teams.away.probablePitcher"
        :to="playerLink(game.teams.away.probablePitcher)"
      >
        {{ shortName(game.teams.away.probablePitcher.fullName) }}
      </RouterLink>
      <span
        v-if="game.teams.home.probablePitcher"
        style="padding:4px;opacity:.6;"
        >vs</span
      >
      <RouterLink
        v-if="game.teams.home.probablePitcher"
        :to="playerLink(game.teams.home.probablePitcher)"
      >
        {{ shortName(game.teams.home.probablePitcher.fullName) }}
      </RouterLink>
    </div>
  </div>
</template>

<script>
const recordCache = new Map();
</script>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { gameTime, teamAbbrev, shortName } from '../composables/gameHelpers';

const { game } = defineProps({
  game: {
    type: Object,
    required: true
  }
});

const playerLink = (player) => ({
  name: 'Player',
  params: { id: player.id },
  query: { name: player.fullName }
});


const homeRecord = ref(null);
const awayRecord = ref(null);

async function fetchTeamRecord(teamId, { signal } = {}) {
  if (recordCache.has(teamId)) {
    return recordCache.get(teamId);
  }
  try {
    const response = await fetch(`/api/teams/${teamId}/record/`, { signal });
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    const record = { wins: data.wins, losses: data.losses };
    recordCache.set(teamId, record);
    return record;
  } catch (e) {
    if (e.name !== 'AbortError') {
      console.error(e);
    }
    return null;
  }
}

let controller;

onMounted(async () => {
  controller = new AbortController();
  const [awayRecordRes, homeRecordRes] = await Promise.all([
    fetchTeamRecord(game.teams.away.team.id, { signal: controller.signal }),
    fetchTeamRecord(game.teams.home.team.id, { signal: controller.signal })
  ]);
  awayRecord.value = awayRecordRes;
  homeRecord.value = homeRecordRes;
});

onUnmounted(() => {
  controller?.abort();
});

const rowStyle = {
  background: '#ffffff',
  padding: '10px',
  border: '1px solid rgba(0,0,0,0.1)',
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

