<template>
  <div class="batter-spray-chart spray-chart">
    <div class="chart">
      <h3>Batted Balls</h3>
      <canvas ref="battedBallsCanvas"></canvas>
    </div>
    <div class="chart">
      <h3>Hits</h3>
      <canvas ref="hitsCanvas"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import Chart from 'chart.js/auto';
import { fetchPlayerStatcastBatterData } from '../services/api.js';

const props = defineProps({
  playerId: { type: [String, Number], required: true },
  startDate: String,
  endDate: String,
});

const battedBallsCanvas = ref(null);
const hitsCanvas = ref(null);
let battedBallsChart;
let hitsChart;

// Batted-ball and hit events from baseball_data_lab constants
const battedBallEvents = [
  'single',
  'double',
  'triple',
  'home_run',
  'field_out',
  'grounded_into_double_play',
  'force_out',
  'sac_fly',
  'sac_bunt',
  'field_error',
  'double_play',
  'triple_play',
  'catcher_interf',
  'fielders_choice',
];

const hitEvents = ['single', 'double', 'triple', 'home_run'];

// Transform Statcast coordinates similar to the BattingSprayChart class
function transformStatcast(data) {
  return data
    .filter(
      (d) => battedBallEvents.includes(d.events) && d.hc_x != null && d.hc_y != null,
    )
    .map((d) => ({
      x: d.hc_x - 125.42,
      y: 198.27 - d.hc_y,
      result: d.events,
    }));
}

// Styling for different events
const eventStyles = {
  single: { color: '#1f77b4', label: 'Single' },
  double: { color: '#2ca02c', label: 'Double' },
  triple: { color: '#ff7f0e', label: 'Triple' },
  home_run: { color: '#d62728', label: 'Home Run' }
};
const outStyle = { color: '#666666', label: 'Out' };

function buildDatasets(points) {
  const grouped = {};
  points.forEach((pt) => {
    const key = eventStyles[pt.result] ? pt.result : 'out';
    if (!grouped[key]) grouped[key] = [];
    grouped[key].push({ x: pt.x, y: pt.y });
  });
  return Object.keys(grouped).map((result) => {
    const style = eventStyles[result] || outStyle;
    return {
      label: style.label,
      data: grouped[result],
      backgroundColor: style.color,
    };
  });
}

// Compute scale bounds based on data, similar to the Python implementation
function scaleBounds(data) {
  if (!data.length) {
    return {
      x: { min: -200, max: 200 },
      y: { min: 0, max: 250 },
    };
  }
  const xs = data.map((p) => p.x);
  const ys = data.map((p) => p.y);
  return {
    x: { min: Math.min(...xs) - 10, max: Math.max(...xs) + 10 },
    // Ensure home plate (0,0) is at the bottom of the chart
    y: {
      min: Math.min(...ys) > 0 ? 0 : Math.min(...ys) - 10,
      max: Math.max(...ys) + 10,
    },
  };
}

// Plugin to draw the diamond baselines using Chart.js
const diamondPlugin = {
  id: 'diamondPlugin',
  afterDraw(chart) {
    const { ctx, scales: { x, y } } = chart;
    const diamondSize = (x.max - x.min) * 0.2;
    const home = { x: 0, y: 0 };
    const first = { x: diamondSize, y: diamondSize };
    const third = { x: -diamondSize, y: diamondSize };
    const second = { x: 0, y: diamondSize * 2 };

    ctx.save();
    ctx.strokeStyle = '#d3d3d3';
    ctx.beginPath();
    ctx.moveTo(x.getPixelForValue(home.x), y.getPixelForValue(home.y));
    ctx.lineTo(x.getPixelForValue(first.x), y.getPixelForValue(first.y));
    ctx.moveTo(x.getPixelForValue(home.x), y.getPixelForValue(home.y));
    ctx.lineTo(x.getPixelForValue(third.x), y.getPixelForValue(third.y));
    ctx.moveTo(x.getPixelForValue(first.x), y.getPixelForValue(first.y));
    ctx.lineTo(x.getPixelForValue(second.x), y.getPixelForValue(second.y));
    ctx.lineTo(x.getPixelForValue(third.x), y.getPixelForValue(third.y));
    ctx.stroke();
    ctx.restore();
  }
};

function createChart(canvas, data, bounds) {
  return new Chart(canvas, {
    type: 'scatter',
    data: { datasets: buildDatasets(data) },
    options: {
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
        },
      },
      scales: bounds,
    },
    plugins: [diamondPlugin],
  });
}

async function loadData() {
  const year = new Date().getFullYear();
  const start = props.startDate || `${year}-03-01`;
  const end = props.endDate || new Date().toISOString().slice(0, 10);
  const res = await fetchPlayerStatcastBatterData(props.playerId, start, end);
  const raw = Array.isArray(res?.results) ? res.results : [];
  const sprayData = transformStatcast(raw);
  const hitsData = sprayData.filter((p) => hitEvents.includes(p.result));
  const bounds = scaleBounds(sprayData);

  if (battedBallsCanvas.value) {
    battedBallsChart?.destroy();
    battedBallsChart = createChart(battedBallsCanvas.value, sprayData, bounds);
  }
  if (hitsCanvas.value) {
    hitsChart?.destroy();
    hitsChart = createChart(hitsCanvas.value, hitsData, bounds);
  }
}

onMounted(loadData);

onBeforeUnmount(() => {
  battedBallsChart?.destroy();
  hitsChart?.destroy();
});
</script>

<style scoped>
.batter-spray-chart {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  justify-content: center;
}
.chart {
  position: relative;
  width: 400px;
  height: 400px;
}
.chart h3 {
  text-align: center;
}
.chart canvas {
  width: 300px !important;
  height: 300px !important;
}
</style>

