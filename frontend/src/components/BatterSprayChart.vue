<template>
  <div class="batter-spray-chart">
    <canvas ref="canvasEl"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import Chart from 'chart.js/auto';

const canvasEl = ref(null);
let chartInstance;

// Dummy spray chart data points
const sprayData = [
  { x: -30, y: 80 },
  { x: 20, y: 70 },
  { x: -60, y: 110 },
  { x: 50, y: 90 },
  { x: 0, y: 120 }
];

onMounted(() => {
  if (canvasEl.value) {
    chartInstance = new Chart(canvasEl.value, {
      type: 'scatter',
      data: {
        datasets: [
          {
            label: 'Spray Chart',
            data: sprayData,
            backgroundColor: 'rgba(75, 192, 192, 1)'
          }
        ]
      },
      options: {
        maintainAspectRatio: false,
        scales: {
          x: {
            min: -150,
            max: 150
          },
          y: {
            min: 0,
            max: 150
          }
        }
      }
    });
  }
});

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy();
  }
});
</script>

<style scoped>
.batter-spray-chart {
  position: relative;
  width: 100%;
  max-width: 500px;
  height: 400px;
  margin: 0 auto;
}
</style>

