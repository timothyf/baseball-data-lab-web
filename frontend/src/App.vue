<template>
  <div>
    <router-view />
    <HelloComponent />
  </div>
</template>

<script>
import HelloComponent from './components/HelloComponent.vue';

export default {
  name: 'App',
  components: {
    HelloComponent
  }
};
</script>
