<script setup lang="ts">
// https://bulma.io/documentation/elements/notification/

// https://vuejs.org/guide/typescript/composition-api.html#typing-component-props
// Note absence of angle brackets below:
const props = defineProps({
  type: {
    type: String,
    default: "info",
    required: false,
  },
  isCloseable: {
    type: Boolean,
    default: false,
    requied: false,
  }
});
</script>

<template>
  <div :class="`notification is-${props.type}`">
    <button v-if="props.isCloseable" class="delete"></button>
    <slot></slot>
  </div>
</template>