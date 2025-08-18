import { createApp } from 'vue';
import HelloComponent from './HelloComponent.vue';

const app = createApp({});
app.component('hello-component', HelloComponent);
app.mount('#vue-app');
