<template>
  <div class="game-row">
    <div class="game-teams">
      <span
        class="team-chip away"
      >
        <img
          v-if="game.teams.away.team.logo_url"
          :src="game.teams.away.team.logo_url"
          alt=""
          class="team-logo"
        />
        {{ teamAbbrev(game.teams.away.team) }}
        <span v-if="awayRecord" class="team-record">{{ awayRecord.wins }}-{{ awayRecord.losses }}</span>
      </span>
      <span class="at-separator">@</span>
      <span
        class="team-chip home"
      >
        <img
          v-if="game.teams.home.team.logo_url"
          :src="game.teams.home.team.logo_url"
          alt=""
          class="team-logo"
        />
        {{ teamAbbrev(game.teams.home.team) }}
        <span v-if="homeRecord" class="team-record">{{ homeRecord.wins }}-{{ homeRecord.losses }}</span>
      </span>
    </div>
    <div class="game-time">
      <RouterLink
        v-if="game.status?.detailedState === 'Final' || game.status?.abstractGameState === 'Live'"
        :to="{ name: 'Game', params: { game_pk: game.gamePk } }"
      >
        {{ gameTime(game) }}
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
      <span v-if="game.decisions?.winner" class="pitcher-result">
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
      <span v-if="game.decisions?.loser" class="pitcher-result">
        <strong>L:</strong>
        <RouterLink :to="playerLink(game.decisions.loser)">
          {{ shortName(game.decisions.loser.fullName) }}
        </RouterLink>
      </span>
      <span v-if="game.decisions?.save" class="pitcher-result">
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
        class="vs-separator"
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

<script setup>
import { ref, onMounted } from 'vue';
import { gameTime, teamAbbrev, shortName } from '../composables/gameHelpers';
import { useStandingsStore } from '../store/standings';

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

const standingsStore = useStandingsStore();

onMounted(async () => {
  const [awayRecordRes, homeRecordRes] = await Promise.all([
    standingsStore.fetchTeamRecord(game.teams.away.team.id),
    standingsStore.fetchTeamRecord(game.teams.home.team.id)
  ]);
  awayRecord.value = awayRecordRes;
  homeRecord.value = homeRecordRes;
});
</script>

<style scoped>
.game-row {
  display: flex;
  align-items: center;
  background: #ffffff;
  padding: 10px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 6px;
  gap: 10px;
  font-size: 0.85rem;
  line-height: 1.1;
  color: #000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.team-chip {
  display: inline-flex;
  align-items: center;
  padding: 2px 6px;
  background: #ffffff;
  color: var(--color-primary);
  border-radius: 4px;
}

.team-chip.away {
  margin-right: 4px;
}

.team-chip.home {
  margin-left: 4px;
}

.team-record {
  margin-left: 4px;
  color: #888;
}

.at-separator {
  padding: 0 4px;
  opacity: 0.6;
  font-size: 1rem;
}

.pitcher-result {
  padding: 4px;
}

.vs-separator {
  padding: 4px;
  opacity: 0.6;
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

