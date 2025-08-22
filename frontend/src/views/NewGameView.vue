<template>
  <div class="game-view container mx-auto p-4">
    <!-- Header: teams & meta -->
    <Card class="mb-4">
      <template #title>
        <div class="flex items-center justify-between gap-4 flex-wrap">
          <!-- Left team -->
          <div class="flex items-center gap-3">
            <img :src="game.away.logo" alt="Away Logo" class="w-12 h-12 object-contain" style="max-width: 75px;" />
            <div>
              <div class="text-sm text-muted-color">Away</div>
              <div class="text-xl font-semibold">{{ game.away.name }}</div>
            </div>
          </div>

          <!-- Score + date/venue -->
          <div class="text-center">
            <div class="text-3xl font-bold leading-none">
              {{ game.away.runs }} <span class="text-muted-color">–</span> {{ game.home.runs }}
            </div>
            <div class="mt-1 text-sm text-muted-color">
              {{ game.gameDate }} • {{ game.venue }} • Final
            </div>
          </div>

          <!-- Right team -->
          <div class="flex items-center gap-3">
            <div class="text-right">
              <div class="text-sm text-muted-color">Home</div>
              <div class="text-xl font-semibold">{{ game.home.name }}</div>
            </div>
            <img :src="game.home.logo" alt="Home Logo" class="w-12 h-12 object-contain" style="max-width: 75px;" />
          </div>
        </div>
      </template>

      <template #content>
        <div class="grid md:grid-cols-2 gap-4">
          <Card>
            <template #title>Linescore</template>
            <template #content>
              <DataTable :value="linescoreRows" size="small" responsiveLayout="scroll">
                <Column field="team" header="Team" frozen />
                <Column v-for="i in 9" :key="i" :field="`i${i}`" :header="`${i}`" class="text-center" />
                <Column field="r" header="R" class="font-semibold text-center" />
                <Column field="h" header="H" class="text-center" />
                <Column field="e" header="E" class="text-center" />
              </DataTable>
            </template>
          </Card>

          <Card>
            <template #title>Game Summary</template>
            <template #content>
              <div class="space-y-2 text-sm">
                <div><span class="font-medium">Winning P:</span> {{ game.summary.winningPitcher }}</div>
                <div><span class="font-medium">Losing P:</span> {{ game.summary.losingPitcher }}</div>
                <div><span class="font-medium">Save:</span> {{ game.summary.savePitcher || '—' }}</div>
                <div><span class="font-medium">HR:</span> {{ game.summary.homers.join(', ') || '—' }}</div>
                <div><span class="font-medium">Attendance:</span> {{ game.summary.attendance.toLocaleString() }}</div>
                <div><span class="font-medium">Time:</span> {{ game.summary.duration }}</div>
              </div>
            </template>
          </Card>
        </div>
      </template>
    </Card>

    <!-- Tabs for Boxscore / Advanced / Plays -->
    <TabView>
      <!-- Boxscore -->
      <TabPanel header="Boxscore">
        <div class="grid md:grid-cols-2 gap-4">
          <Card>
            <template #title>Batting — {{ game.away.abbrev }}</template>
            <template #content>
              <DataTable :value="game.boxscore.away.batting" size="small" responsiveLayout="scroll">
                <Column field="name" header="Player" />
                <Column field="pos" header="Pos" class="text-center" />
                <Column field="ab" header="AB" class="text-center" />
                <Column field="r" header="R" class="text-center" />
                <Column field="h" header="H" class="text-center" />
                <Column field="rbi" header="RBI" class="text-center" />
                <Column field="bb" header="BB" class="text-center" />
                <Column field="so" header="SO" class="text-center" />
                <Column field="avg" header="AVG" class="text-center" />
                <Column field="ops" header="OPS" class="text-center" />
              </DataTable>
            </template>
          </Card>

          <Card>
            <template #title>Batting — {{ game.home.abbrev }}</template>
            <template #content>
              <DataTable :value="game.boxscore.home.batting" size="small" responsiveLayout="scroll">
                <Column field="name" header="Player" />
                <Column field="pos" header="Pos" class="text-center" />
                <Column field="ab" header="AB" class="text-center" />
                <Column field="r" header="R" class="text-center" />
                <Column field="h" header="H" class="text-center" />
                <Column field="rbi" header="RBI" class="text-center" />
                <Column field="bb" header="BB" class="text-center" />
                <Column field="so" header="SO" class="text-center" />
                <Column field="avg" header="AVG" class="text-center" />
                <Column field="ops" header="OPS" class="text-center" />
              </DataTable>
            </template>
          </Card>

          <Card>
            <template #title>Pitching — {{ game.away.abbrev }}</template>
            <template #content>
              <DataTable :value="game.boxscore.away.pitching" size="small" responsiveLayout="scroll">
                <Column field="name" header="Pitcher" />
                <Column field="ip" header="IP" class="text-center" />
                <Column field="h" header="H" class="text-center" />
                <Column field="r" header="R" class="text-center" />
                <Column field="er" header="ER" class="text-center" />
                <Column field="bb" header="BB" class="text-center" />
                <Column field="so" header="SO" class="text-center" />
                <Column field="hr" header="HR" class="text-center" />
                <Column field="pc" header="PC" class="text-center" />
                <Column field="era" header="ERA" class="text-center" />
              </DataTable>
            </template>
          </Card>

          <Card>
            <template #title>Pitching — {{ game.home.abbrev }}</template>
            <template #content>
              <DataTable :value="game.boxscore.home.pitching" size="small" responsiveLayout="scroll">
                <Column field="name" header="Pitcher" />
                <Column field="ip" header="IP" class="text-center" />
                <Column field="h" header="H" class="text-center" />
                <Column field="r" header="R" class="text-center" />
                <Column field="er" header="ER" class="text-center" />
                <Column field="bb" header="BB" class="text-center" />
                <Column field="so" header="SO" class="text-center" />
                <Column field="hr" header="HR" class="text-center" />
                <Column field="pc" header="PC" class="text-center" />
                <Column field="era" header="ERA" class="text-center" />
              </DataTable>
            </template>
          </Card>
        </div>
      </TabPanel>

      <!-- Advanced -->
      <TabPanel header="Advanced">
        <div class="grid md:grid-cols-3 gap-4">
          <Card class="md:col-span-2">
            <template #title>Win Probability (WPA)</template>
            <template #content>
              <Chart type="line" :data="wpaChartData" :options="wpaChartOpts" />
              <div class="text-xs text-muted-color mt-2">
                WPA by play (home team perspective). Hover for details.
              </div>
            </template>
          </Card>

          <Card>
            <template #title>Game Leverage</template>
            <template #content>
              <DataTable :value="leverageRows" size="small" responsiveLayout="scroll">
                <Column field="inning" header="Inn" class="text-center" />
                <Column field="desc" header="Event" />
                <Column field="li" header="LI" class="text-center" />
                <Column field="wpa" header="WPA" class="text-center" />
              </DataTable>
            </template>
          </Card>

          <Card>
            <template #title>Pitch Mix — {{ game.advanced.away.sp.name }}</template>
            <template #content>
              <DataTable :value="game.advanced.away.pitchMix" size="small" responsiveLayout="scroll">
                <Column field="pitch" header="Pitch" />
                <Column field="usage" header="Usage%" class="text-center" />
                <Column field="velo" header="Velo" class="text-center" />
                <Column field="whiff" header="Whiff%" class="text-center" />
              </DataTable>
            </template>
          </Card>

          <Card>
            <template #title>Pitch Mix — {{ game.advanced.home.sp.name }}</template>
            <template #content>
              <DataTable :value="game.advanced.home.pitchMix" size="small" responsiveLayout="scroll">
                <Column field="pitch" header="Pitch" />
                <Column field="usage" header="Usage%" class="text-center" />
                <Column field="velo" header="Velo" class="text-center" />
                <Column field="whiff" header="Whiff%" class="text-center" />
              </DataTable>
            </template>
          </Card>
        </div>
      </TabPanel>

      <!-- Plays / Key Moments -->
      <TabPanel header="Plays & Key Moments">
        <div class="grid md:grid-cols-2 gap-4">
          <Card>
            <template #title>Scoring Plays</template>
            <template #content>
              <Timeline :value="scoringTimeline">
                <template #marker="{ item }">
                  <Tag :value="item.inn" severity="info" />
                </template>
                <template #content="{ item }">
                  <div class="font-medium">{{ item.desc }}</div>
                  <div class="text-sm text-muted-color">{{ item.away }}–{{ item.home }} {{ item.score }}</div>
                </template>
              </Timeline>
            </template>
          </Card>

          <Card>
            <template #title>Play-by-Play</template>
            <template #content>
              <Accordion>
                <AccordionTab v-for="(inn, idx) in pbpByInning" :key="idx" :header="`Inning ${inn.inning}`">
                  <ul class="list-disc pl-6">
                    <li v-for="(p, i) in inn.plays" :key="i" class="mb-1">{{ p }}</li>
                  </ul>
                </AccordionTab>
              </Accordion>
            </template>
          </Card>
        </div>
      </TabPanel>
    </TabView>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// PrimeVue components
import Card from 'primevue/card'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'
import Timeline from 'primevue/timeline'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import Accordion from 'primevue/accordion'
import AccordionTab from 'primevue/accordiontab'
import Chart from 'primevue/chart'

// Mock data loader (replace with real API calls)
const game = ref({
  gameDate: 'Aug 12, 2024',
  venue: 'T-Mobile Park',
  away: { abbrev: 'DET', name: 'Detroit Tigers', logo: 'https://www.mlbstatic.com/team-logos/team-cap-on-light/118.svg', runs: 3 },
  home: { abbrev: 'SEA', name: 'Seattle Mariners', logo: 'https://www.mlbstatic.com/team-logos/team-cap-on-light/118.svg', runs: 4 },
  summary: {
    winningPitcher: 'Luis Castillo (SEA)',
    losingPitcher: 'Tarik Skubal (DET)',
    savePitcher: '—',
    homers: ['J Rodríguez (SEA)'],
    attendance: 33321,
    duration: '2:41'
  },
  linescore: {
    away: [0,0,1,0,0,0,2,0,0], home: [0,1,0,0,0,1,2,0,0],
    ahre: { r: 3, h: 7, e: 0 }, hhre: { r: 4, h: 8, e: 1 }
  },
  boxscore: {
    away: {
      batting: [
        { name: 'T Greene', pos: 'CF', ab: 4, r: 1, h: 2, rbi: 1, bb: 0, so: 1, avg: '.275', ops: '.840' },
        // ...
      ],
      pitching: [
        { name: 'T Skubal', ip: '6.1', h: 6, r: 3, er: 3, bb: 1, so: 8, hr: 1, pc: 101, era: '3.12' },
        // ...
      ]
    },
    home: {
      batting: [
        { name: 'J Rodríguez', pos: 'CF', ab: 4, r: 1, h: 2, rbi: 2, bb: 0, so: 1, avg: '.291', ops: '.873' },
        // ...
      ],
      pitching: [
        { name: 'L Castillo', ip: '7.0', h: 6, r: 2, er: 2, bb: 1, so: 7, hr: 0, pc: 98, era: '3.20' },
        // ...
      ]
    }
  },
  advanced: {
    away: { sp: { name: 'T Skubal' }, pitchMix: [
      { pitch: '4-Seam', usage: 41, velo: '96.5', whiff: 28 },
      { pitch: 'Change', usage: 24, velo: '87.8', whiff: 32 },
      { pitch: 'Slider', usage: 35, velo: '88.9', whiff: 30 },
    ]},
    home: { sp: { name: 'L Castillo' }, pitchMix: [
      { pitch: '4-Seam', usage: 38, velo: '97.1', whiff: 26 },
      { pitch: 'Sinker', usage: 22, velo: '97.5', whiff: 18 },
      { pitch: 'Slider', usage: 40, velo: '87.4', whiff: 31 },
    ]}
  }
})

const linescoreRows = computed(() => {
  const a = game.value.linescore
  const mapRow = (abbr, arr, totals) => ({
    team: abbr,
    i1: arr[0], i2: arr[1], i3: arr[2], i4: arr[3], i5: arr[4], i6: arr[5], i7: arr[6], i8: arr[7], i9: arr[8],
    r: totals.r, h: totals.h, e: totals.e
  })
  return [
    mapRow(game.value.away.abbrev, a.away, a.ahre),
    mapRow(game.value.home.abbrev, a.home, a.hhre)
  ]
})

// WPA chart (PrimeVue uses Chart.js)
const wpaChartData = ref({
  labels: Array.from({ length: 20 }, (_, i) => `P${i+1}`),
  datasets: [
    {
      label: 'Home Win Prob.',
      data: [50, 48, 52, 47, 49, 51, 60, 58, 62, 65, 63, 61, 55, 53, 57, 59, 62, 64, 66, 70],
      fill: false,
      tension: 0.3
    }
  ]
})
const wpaChartOpts = ref({
  responsive: true,
  plugins: {
    legend: { display: true },
    tooltip: { mode: 'index', intersect: false }
  },
  scales: {
    y: { min: 0, max: 100, ticks: { callback: (v) => v + '%' } }
  }
})

// Leverage events (example)
const leverageRows = ref([
  { inning: '7th', desc: '2 on, 1 out — tie game', li: 3.1, wpa: '+12%' },
  { inning: '8th', desc: 'Go-ahead HR', li: 2.7, wpa: '+18%' },
  { inning: '9th', desc: 'Closer enters, tying run on 2nd', li: 2.9, wpa: '-6%' }
])

// Scoring timeline & PBP
const scoringTimeline = ref([
  { inn: '2', desc: 'SEA scores 1 on single', away: 0, home: 1, score: 'SEA 1–0' },
  { inn: '6', desc: 'DET ties on RBI 2B', away: 1, home: 1, score: '1–1' },
  { inn: '7', desc: 'SEA 2-run HR', away: 1, home: 3, score: 'SEA 3–1' },
  { inn: '7', desc: 'DET 2-run rally', away: 3, home: 3, score: '3–3' },
  { inn: '8', desc: 'SEA takes lead on sac fly', away: 3, home: 4, score: 'SEA 4–3' }
])
const pbpByInning = ref([
  { inning: 1, plays: ['Groundout', 'Single to RF', 'Strikeout swinging', 'Flyout to CF'] },
  { inning: 2, plays: ['HR to LF (SEA 1–0)', 'Walk', 'Double Play 6-4-3'] },
  // ...
])

onMounted(() => {
  // Replace with real fetches; hydrate logos, linescore, boxscore, advanced stats, etc.
  // loadGame(gamePk)
})

</script>

<style scoped>
.container { max-width: 1200px; }
.text-muted-color { color: var(--text-color-secondary); }
</style>
