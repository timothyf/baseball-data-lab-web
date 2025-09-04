<template>
  <Dialog
    :visible="visible"
    modal
    :closable="false"
    :draggable="false"
    :dismissableMask="false"
    :closeOnEscape="false"
    class="loading-dialog"
  >
    <div class="loading-content">
      <ProgressSpinner />
      <p>Loading data...</p>
    </div>
  </Dialog>
</template>

<script setup>
import Dialog from 'primevue/dialog';
import 'primevue/dialog/style';
import ProgressSpinner from 'primevue/progressspinner';
import 'primevue/progressspinner/style';

defineProps({
  visible: {
    type: Boolean,
    default: false,
  },
});
</script>

<style scoped>
.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
}
</style>

