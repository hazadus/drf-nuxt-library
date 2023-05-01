<script setup lang="ts">
const config = useRuntimeConfig();
console.log("Library app started. API base is " + config.public.apiBase);
</script>

<template>
  <TheNavBar />
  <section class="section p-5 page-content-section">
    <div class="container is-widescreen">
      <NuxtPage />
    </div>
  </section>
  <TheFooter />
</template>

<style>
@import 'bulma/css/bulma.css';

.page-content-section {
  min-height: calc(100vh - 56px - 168px);
}
</style>