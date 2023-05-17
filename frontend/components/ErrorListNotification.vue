<script setup lang="ts">
const props = defineProps({
  errors: {
    type: Object,
    required: true,
  },
});
</script>

<template>
  <BulmaNotification v-if="errors.length" type="danger">
    <div class="content">
      <div class="icon-text mb-3">
        <span class="icon has-text-warning is-hidden-mobile">
          <Icon name="mdi:exclamation" />
        </span>
        <span>
          <b>При обращении к серверу произошла ошибка!</b> Попробуйте перезагрузить страницу в браузере.
        </span>
      </div>
      <ul>
        <template v-for="error in errors">
          <li v-for="value, key in error">
            {{ key }}: {{ value }}
          </li>
        </template>
      </ul>
    </div>
  </BulmaNotification>
</template>