<template>
  <div class="game-row" :style="rowStyle">
    <div class="game-teams">
      <span
        class="team-chip away"
        style="display:inline-flex;align-items:center;padding:2px 6px;margin-right:4px;background:#ffffff;"
      >
        <img
          v-if="game.teams.away.team.logo_url"
          :src="game.teams.away.team.logo_url"
          alt=""
          class="team-logo"
        />
        {{ teamAbbrev(game.teams.away.team) }}
      </span>
      <span style="padding:0 4px;opacity:.6;font-size:1.0rem">@</span>
      <span
        class="team-chip home"
        style="display:inline-flex;align-items:center;padding:2px 6px;margin-left:4px;background:#ffffff;"
      >
        <img
          v-if="game.teams.home.team.logo_url"
          :src="game.teams.home.team.logo_url"
          alt=""
          class="team-logo"
        />
        {{ teamAbbrev(game.teams.home.team) }}
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

<script setup>
import { gameTime, teamAbbrev, shortName } from '../composables/gameHelpers';

const { game } = defineProps({
  game: {
    type: Object,
    required: true
  }
});

const rowStyle = {
  background: '#f9fafb',
  padding: '6px 10px',
  border: '1px solid #e2e8f0',
  borderRadius: '6px',
  marginLeft: 'auto',
  display: 'flex',
  alignItems: 'center',
  gap: '10px',
  fontSize: '.75rem',
  lineHeight: '1.1',
  boxShadow: '0 1px 2px rgba(0,0,0,0.04)'
};
</script>

<style scoped>
.game-row {
  display: flex;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}

.game-teams {
  width: 250px;
  font-weight: 600;
}

.game-time {
  width: 80px;
}

.game-score {
  width: 60px;
  font-weight: 600;
  text-align: center;
}

.game-broadcasts {
  flex: 1;
  font-size: 0.9rem;
  color: #555;
}

.game-pitchers {
  width: 270px;
  font-size: 0.9rem;
  color: #555;
  text-align: right;
}

.team-logo {
  width: 20px;
  height: 20px;
  margin-right: 4px;
}
</style>

