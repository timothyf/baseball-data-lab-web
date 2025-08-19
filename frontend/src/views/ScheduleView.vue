<template>
  <div v-if="scheduleStore.schedule && scheduleStore.schedule.length">
    <div class="schedule-header">
      <button class="nav-btn" @click="prevDay">&#8592;</button>
      <h2 class="header-date">{{ formatDate(currentDate) }}</h2>
      <button class="nav-btn" @click="nextDay">&#8594;</button>
    </div>
    <div v-for="(day, dIndex) in scheduleStore.schedule" :key="dIndex" class="schedule-day">
      <ul class="game-list">
        <li v-for="game in day.games" :key="game.gamePk" class="game-row"
            :style="{
              background:'#f9fafb',
              padding:'6px 10px',
              border:'1px solid #e2e8f0',
              borderRadius:'6px',
              marginLeft:'auto',
              display:'flex',
              alignItems:'center',
              gap:'10px',
              // justifyContent:'flex-end',
              fontSize:'.75rem',
              lineHeight:'1.1',
              boxShadow:'0 1px 2px rgba(0,0,0,0.04)'
            }">
          <div class="game-teams">
            <span class="team-chip away" style="display:inline-flex;align-items:center;padding:2px 6px;margin-right:4px;background:#ffffff;">
              <img v-if="game.teams.away.team.logo_url" :src="game.teams.away.team.logo_url" alt="" class="team-logo" />
              {{ teamAbbrev(game.teams.away.team) }}
            </span>
            <span style="padding:0 4px;opacity:.6;">@</span>
            <span class="team-chip home" style="display:inline-flex;align-items:center;padding:2px 6px;margin-left:4px;background:#ffffff;">
              <img v-if="game.teams.home.team.logo_url" :src="game.teams.home.team.logo_url" alt="" class="team-logo" />
              {{ teamAbbrev(game.teams.home.team) }}
            </span>
          </div>
          <div class="game-time">{{ gameTime(game) }}</div>
          <div class="game-score" v-if="game.status?.detailedState === 'Final'">
            {{ game.teams.away.score }} - {{ game.teams.home.score }}
          </div>
          <div class="game-broadcasts" v-if="game.broadcasts && game.broadcasts.length">
            {{ game.broadcasts.map(b => b.callSign || b.name).join(', ') }}
            </div>
            <div
            class="game-pitchers"
            v-if="game.status?.detailedState === 'Final'"
            >
            <span v-if="game.decisions?.winner">
              <strong>W:</strong> {{ shortName(game.decisions.winner.fullName) }}
            </span>
            <span v-if="game.decisions?.loser">
              <strong>L:</strong> {{ shortName(game.decisions.loser.fullName) }}
            </span>
            </div>
            <div
            class="game-pitchers"
            v-else
            >
            <span v-if="game.teams.away.probablePitcher">
              {{ shortName(game.teams.away.probablePitcher.fullName) }}
            </span>
            <span v-if="game.teams.home.probablePitcher" style="opacity:.6;">vs</span>
            <span v-if="game.teams.home.probablePitcher">
              {{ shortName(game.teams.home.probablePitcher.fullName) }}
            </span>
            </div>
          </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { scheduleStore } from '../store/schedule';

const currentDate = ref(
  (scheduleStore.schedule[0]?.date || scheduleStore.schedule[0]?.games[0]?.gameDate)?.slice(0, 10)
);

async function fetchSchedule(dateStr) {
  const resp = await fetch(`/api/schedule/?date=${dateStr}`);
  const data = await resp.json();
  scheduleStore.schedule = data;
  if (data && data.length) {
    const d = data[0].date || data[0].games[0]?.gameDate;
    currentDate.value = d ? d.slice(0, 10) : dateStr;
  }
}

function adjustDay(delta) {
  const date = new Date(currentDate.value);
  date.setDate(date.getDate() + delta);
  const iso = date.toISOString().split('T')[0];
  currentDate.value = iso;
  fetchSchedule(iso);
}

function prevDay() {
  adjustDay(-1);
}

function nextDay() {
  adjustDay(1);
}

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
  width: 200px;
  font-size: 0.9rem;
  color: #555;
  text-align: right;
}

.team-name {
  font-weight: bold;
  color: #333;
}

.team-logo {
  width: 20px;
  height: 20px;
  margin-right: 4px;
}

.schedule-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.header-date {
  flex: 1;
  text-align: center;
  margin: 0;
}

.nav-btn {
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
}
</style>

