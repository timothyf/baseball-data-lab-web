<template>
  <section class="team-view" :style="teamColorStyle">
    <div class="team-container">
      <TeamHeader :team-logo-src="teamLogoSrc" :team-record="teamRecord" />
      <TabView>
        <TabPanel header="Summary">
          <div class="summary-content">
            <p class="venue-name" v-if="teamDetails">
              {{ teamDetails.venue?.name }} • {{ teamDetails.location_name }}
            </p>
            <Skeleton v-else width="300px" height="1.5rem" />
          </div>
          <div v-if="divisionStandings.length" class="stats-container">
            <table class="team-stats division-standings">
              <thead>
                <tr>
                  <th>Team</th>
                  <th>W</th>
                  <th>L</th>
                  <th>PCT</th>
                  <th>GB</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="record in divisionStandings" :key="record.team.id"
                  :class="{ 'current-team': record.team.id == mlbam_team_id }">
                  <td>{{ record.team.name }}</td>
                  <td>{{ record.wins }}</td>
                  <td>{{ record.losses }}</td>
                  <td>{{ record.winningPercentage }}</td>
                  <td>{{ record.divisionGamesBack }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </TabPanel>
        <TabPanel header="Leaders">
          <TeamLeaders :leaders="leaders" />
        </TabPanel>
        <TabPanel header="Roster">
          <TeamRoster :roster="roster" />
        </TabPanel>
        <TabPanel header="Stats">
          Content coming soon...
        </TabPanel>
        <TabPanel header="Schedule">
          <TeamSchedule :recent-schedule="recentSchedule" :mlbam-team-id="mlbam_team_id" />
        </TabPanel>
        <TabPanel header="History">
          Content coming soon...
        </TabPanel>
      </TabView>
    </div>
    <LoadingDialog :visible="loading" />
  </section>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
import Skeleton from 'primevue/skeleton';
import LoadingDialog from '../components/LoadingDialog.vue';
import TeamHeader from '../components/team/TeamHeader.vue';
import TeamLeaders from '../components/team/TeamLeaders.vue';
import TeamRoster from '../components/team/TeamRoster.vue';
import TeamSchedule from '../components/team/TeamSchedule.vue';
import teamColors from '../data/teamColors.json';
import { useTeamsStore } from '../store/teams';
import { useCachedFetch } from '../composables/useCachedFetch';
import deepEqual from '../utils/deepEqual.js';
import {
  fetchTeamLogo,
  fetchTeamRecord,
  fetchStandings,
  fetchTeamDetails,
  fetchTeamRecentSchedule,
  fetchTeamRoster,
  fetchTeamLeaders,
} from '../services/api.js';

const { mlbam_team_id, name } = defineProps({
  mlbam_team_id: { type: String, required: true },
  name: { type: String, required: false }
});

const teamLogoSrc = ref("");
const teamRecord = ref(null);
const recentSchedule = ref(null);
const roster = ref([]);
const teamDetails = ref(null);
const divisionStandings = ref([]);
const leaders = ref(null);
const loading = ref(true);
const teamsStore = useTeamsStore();

const teamColorStyle = computed(() => {
  const colors = teamColors[name] || [];
  return {
    '--color-primary': colors[0]?.hex || '#1e3a8a',
    '--color-secondary': colors[1]?.hex || '#1e40af',
    '--color-accent': colors[2]?.hex || '#1e3a8a'
  };
});

async function loadLogo(mlbam_team_id) {
  const url = await fetchTeamLogo(mlbam_team_id);
  teamLogoSrc.value = (url || "").trim();
}

async function loadRecord(mlbam_team_id, force = false) {
  await useCachedFetch({
    getter: () => teamsStore.getStandings(mlbam_team_id),
    setter: (data) => teamsStore.setStandings(mlbam_team_id, data),
    fetcher: async () => {
      const [record, standings] = await Promise.all([
        fetchTeamRecord(mlbam_team_id),
        loadStandings(mlbam_team_id),
      ]);
      return { record, standings };
    },
    assign: ({ record, standings }) => {
      teamRecord.value = record;
      divisionStandings.value = standings;
    },
    force,
  });
}

async function loadStandings(mlbam_team_id) {
  const data = await fetchStandings();
  const records = data?.records || data || [];
  const division = records.find(r =>
    r.teamRecords?.some(record => record.team.id === Number(mlbam_team_id))
  );
  return division?.teamRecords || [];
}

async function resolveTeamId(mlbam_team_id) {
  loading.value = true;
  await Promise.all([
    loadLogo(mlbam_team_id).catch(() => {}),
    loadRecord(mlbam_team_id).catch(() => {}),
    loadTeamDetails(mlbam_team_id).catch(() => {}),
    loadRecentSchedule(mlbam_team_id).catch(() => {}),
    loadRoster(mlbam_team_id).catch(() => {}),
    loadLeaders(mlbam_team_id).catch(() => {}),
  ]);
  loading.value = false;
}

onMounted(() => {
  resolveTeamId(mlbam_team_id);
});

watch(
  () => mlbam_team_id,
  (newId, oldId) => {
    if (deepEqual(newId, oldId)) return;

    teamLogoSrc.value = "";
    teamRecord.value = null;
    recentSchedule.value = null;
    roster.value = [];
    teamDetails.value = null;
    divisionStandings.value = [];
    leaders.value = null;

    resolveTeamId(newId);
  }
);

async function loadRecentSchedule(mlbam_team_id) {
  recentSchedule.value = await fetchTeamRecentSchedule(mlbam_team_id);
}

async function loadRoster(mlbam_team_id, force = false) {
  await useCachedFetch({
    getter: () => teamsStore.getRoster(mlbam_team_id),
    setter: (data) => teamsStore.setRoster(mlbam_team_id, data),
    fetcher: async () => {
      const data = await fetchTeamRoster(mlbam_team_id);
      return data?.roster ?? data ?? [];
    },
    assign: roster,
    force,
  });
}

async function loadLeaders(mlbam_team_id, force = false) {
  await useCachedFetch({
    getter: () => teamsStore.getLeaders(mlbam_team_id),
    setter: (data) => teamsStore.setLeaders(mlbam_team_id, data),
    fetcher: async () => await fetchTeamLeaders(mlbam_team_id) || null,
    assign: leaders,
    force,
  });
}

async function loadTeamDetails(mlbam_team_id, force = false) {
  await useCachedFetch({
    getter: () => teamsStore.getDetails(mlbam_team_id),
    setter: (data) => teamsStore.setDetails(mlbam_team_id, data),
    fetcher: async () => await fetchTeamDetails(mlbam_team_id) || null,
    assign: teamDetails,
    force,
  });
}
</script>

<style scoped>
.team-view {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  color: #fff;
  padding: 2rem 1rem;
}

.team-container {
  max-width: 1100px;
  margin: 0 auto;
}
.division-standings thead th {
  background-color: var(--color-primary);
  color: #fff;
}

.division-standings .current-team td {
  background-color: hsl(210, 100%, 80%);
  color: white;
  font-weight: 600;
}

</style>
