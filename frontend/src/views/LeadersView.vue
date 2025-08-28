<template>
  <section class="leaders-view">
    <div class="leaders-content">
      <h1>League Leaders</h1>
      <div class="leaders-lists">
        <PlayerQuickList
          v-if="leaders?.batting?.HR"
          title="HR Leaders"
          :players="leaders.batting.HR"
        />
        <PlayerQuickList
          v-if="leaders?.batting?.AVG"
          title="AVG Leaders"
          :players="leaders.batting.AVG"
        />
        <PlayerQuickList
          v-if="leaders?.batting?.OPS"
          title="OPS Leaders"
          :players="leaders.batting.OPS"
        />
        <PlayerQuickList
          v-if="leaders?.pitching?.ERA"
          title="ERA Leaders"
          :players="leaders.pitching.ERA"
          :decimal-places="2"
        />
        <PlayerQuickList
          v-if="leaders?.pitching?.SO"
          title="SO Leaders"
          :players="leaders.pitching.SO"
        />
        <PlayerQuickList
          v-if="leaders?.pitching?.WHIP"
          title="WHIP Leaders"
          :players="leaders.pitching.WHIP"
          :decimal-places="2"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import PlayerQuickList from '../components/PlayerQuickList.vue';

const leaders = ref(null);

onMounted(async () => {
  try {
    const res = await fetch('/api/leaders/');
    leaders.value = await res.json();
  } catch (e) {
    console.error('Failed to fetch league leaders:', e);
    leaders.value = null;
  }
});
</script>

<style scoped>
.leaders-view {
  display: flex;
  justify-content: center;
  width: 100%;
}

.leaders-content {
  max-width: 1100px;
}

.leaders-lists {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
}
</style>
