<template>
  <div v-if="scheduleStore.schedule && scheduleStore.schedule.length">
    <div v-for="(day, dIndex) in scheduleStore.schedule" :key="dIndex" class="schedule-day">
      <h2>{{ formatDate(day.date || day.games[0]?.gameDate) }}</h2>
      <ul class="game-list">
        <li v-for="game in day.games" :key="game.gamePk" class="game-row">
          <div class="game-teams">
            <span class="away">{{ teamAbbrev(game.teams.away.team) }}</span>
            <span>@</span>
            <span class="home">{{ teamAbbrev(game.teams.home.team) }}</span>
          </div>
          <div class="game-time">{{ gameTime(game) }}</div>
          <div class="game-broadcasts" v-if="game.broadcasts && game.broadcasts.length">
            {{ game.broadcasts.map(b => b.callSign || b.name).join(', ') }}
          </div>
          <div class="game-pitchers">
            <span v-if="game.teams.away.probablePitcher">
              {{ shortName(game.teams.away.probablePitcher.fullName) }}
            </span>
            <span v-if="game.teams.home.probablePitcher">
              vs {{ shortName(game.teams.home.probablePitcher.fullName) }}
            </span>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { scheduleStore } from '../store/schedule';

function formatDate(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString(undefined, { weekday: 'long', month: 'short', day: 'numeric' });
}

function formatTime(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleTimeString(undefined, { hour: 'numeric', minute: '2-digit' });
}

function gameTime(game) {
  if (game?.status?.abstractGameState === 'Live') return 'LIVE';
  if (game?.status?.detailedState === 'Final') return 'Final';
  return formatTime(game.gameDate);
}

function teamAbbrev(team) {
  return team?.abbreviation || team?.teamCode || team?.name || '';
}

function shortName(name) {
  if (!name) return '';
  const parts = name.split(' ');
  if (parts.length >= 2) {
    return `${parts[0][0]}. ${parts.slice(1).join(' ')}`;
  }
  return name;
}
</script>

<style scoped>
.schedule-day {
  margin-bottom: 1.5rem;
}

.game-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.game-row {
  display: flex;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}

.game-teams {
  width: 150px;
  font-weight: 600;
}

.game-time {
  width: 80px;
}

.game-broadcasts {
  flex: 1;
  font-size: 0.9rem;
  color: #555;
}

.game-pitchers {
  width: 200px;
  font-size: 0.9rem;
  color: #555;
  text-align: right;
}
</style>

