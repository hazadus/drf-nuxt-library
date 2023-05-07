<script setup lang="ts">
import { useAuthStore } from "./stores/AuthStore";

const authStore = useAuthStore();
const config = useRuntimeConfig();
console.log("Library app started. API base is " + config.public.apiBase);

onBeforeMount(() => {
  authStore.initializeStore();
});
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