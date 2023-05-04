<script setup lang="ts">
const searchInputElement: Ref<HTMLInputElement | null> = ref(null);
const searchQuery: Ref<String> = ref("");

onMounted(() => {
  searchInputElement.value?.focus();
});
</script>

<template>
  <!-- Search query input  -->
  <div class="field">
    <div class="control has-icons-left is-large is-loading">
      <input ref="searchInputElement" v-model="searchQuery" @keyup.escape="searchQuery = ''" class="input is-large"
        type="text" placeholder="Печатайте для поиска по всем книгам...">
      <span class="icon is-left">
        <Icon name="mdi:search" />
      </span>
    </div>
  </div>

  <!-- Search results summary -->
  <nav class="level is-mobile">
    <div class="level-item has-text-centered">
      <div>
        <p class="heading">Всего книг</p>
        <p class="title">3,456</p>
      </div>
    </div>
    <div class="level-item has-text-centered">
      <div>
        <p class="heading">Найдено</p>
        <p class="title">123</p>
      </div>
    </div>
    <div class="level-item has-text-centered">
      <div>
        <p class="heading">Найдено в ваших книгах</p>
        <p class="title">456</p>
      </div>
    </div>
  </nav>
</template>