<template>
  <div class="json-node">
    <template v-if="isObject">
      <template v-if="hasLabel">
        <details>
          <summary>{{ label }}</summary>
          <ul>
            <li v-for="(v, k) in data" :key="k">
              <JsonViewer :data="v" :label="k" />
            </li>
          </ul>
        </details>
      </template>
      <template v-else>
        <ul>
          <li v-for="(v, k) in data" :key="k">
            <JsonViewer :data="v" :label="k" />
          </li>
        </ul>
      </template>
    </template>
    <template v-else>
      <span>
        <strong v-if="hasLabel">{{ label }}: </strong>{{ formattedValue }}
      </span>
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue';

defineOptions({ name: 'JsonViewer' });

const props = defineProps({
  data: { type: [Object, Array, String, Number, Boolean, null], required: true },
  label: { type: [String, Number], default: '' }
});

const isObject = computed(() => typeof props.data === 'object' && props.data !== null);
const hasLabel = computed(() => props.label !== '' && props.label !== null);
const formattedValue = computed(() => JSON.stringify(props.data));
</script>

<style scoped>
ul {
  list-style: none;
  padding-left: 1rem;
}

summary {
  cursor: pointer;
}

span {
  font-family: monospace;
}
</style>

