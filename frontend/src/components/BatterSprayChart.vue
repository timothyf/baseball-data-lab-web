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
import diamond from '../assets/diamond.svg';

const battedBallsCanvas = ref(null);
const hitsCanvas = ref(null);
let battedBallsChart;
let hitsChart;

const sprayData = [
  { x: -30, y: 80, result: 'out' },
  { x: 20, y: 70, result: 'single' },
  { x: -60, y: 110, result: 'double' },
  { x: 50, y: 90, result: 'triple' },
  { x: 0, y: 120, result: 'home_run' },
  { x: 30, y: 60, result: 'out' },
  { x: -20, y: 95, result: 'single' },
  { x: 70, y: 130, result: 'home_run' },
  { x: -90, y: 140, result: 'double' },
  { x: 10, y: 50, result: 'out' }
];

const hitsData = sprayData.filter(p => p.result !== 'out');

const colors = {
  single: '#1f77b4',
  double: '#2ca02c',
  triple: '#ff7f0e',
  home_run: '#d62728',
  out: '#666666'
};

const labels = {
  single: 'Single',
  double: 'Double',
  triple: 'Triple',
  home_run: 'Home Run',
  out: 'Out'
};

function buildDatasets(points) {
  const grouped = {};
  points.forEach(pt => {
    if (!grouped[pt.result]) grouped[pt.result] = [];
    grouped[pt.result].push({ x: pt.x, y: pt.y });
  });
  return Object.keys(grouped).map(result => ({
    label: labels[result],
    data: grouped[result],
    backgroundColor: colors[result]
  }));
}

const fieldImage = new Image();
fieldImage.src = diamond;
const fieldPlugin = {
  id: 'diamondBackground',
  beforeDraw(chart) {
    const { ctx, chartArea: { left, top, width, height } } = chart;
    if (fieldImage.complete) {
      ctx.drawImage(fieldImage, left, top, width, height);
    } else {
      fieldImage.onload = () => chart.draw();
    }
  }
};

function createChart(canvas, data) {
  return new Chart(canvas, {
    type: 'scatter',
    data: { datasets: buildDatasets(data) },
    options: {
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        }
      },
      scales: {
        x: { min: -150, max: 150 },
        y: { min: 0, max: 150 }
      }
    },
    plugins: [fieldPlugin]
  });
}

onMounted(() => {
  if (battedBallsCanvas.value) {
    battedBallsChart = createChart(battedBallsCanvas.value, sprayData);
  }
  if (hitsCanvas.value) {
    hitsChart = createChart(hitsCanvas.value, hitsData);
  }
});

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

