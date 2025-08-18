const HelloComponent = {
    template: `<div class="vue-message">This is rendered by a Vue component.</div>`
};

const app = Vue.createApp({});
app.component('hello-component', HelloComponent);
app.mount('#vue-app');
