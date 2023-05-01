<script setup lang="ts">
const route = useRoute();
</script>

<template>
  <Title>
    Подробно о книге | Библиотека
  </Title>

  <h2 class="header is-size-2">
    Подробности о книге - {{ route.params.id }}
  </h2>
</template>