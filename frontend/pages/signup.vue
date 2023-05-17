<script setup lang="ts">
</script>

<template>
  <Title>
    Регистрация | Библиотека
  </Title>

  <!-- Breadcrumbs -->
  <nav class="breadcrumb is-small has-arrow-separator" aria-label="breadcrumbs">
    <ul>
      <li>
        <NuxtLink to="/">
          Главная
        </NuxtLink>
      </li>
      <li class="is-active">
        <NuxtLink to="/signup/">
          Регистрация
        </NuxtLink>
      </li>
    </ul>
  </nav>

  <h2 class="header is-size-2 mb-5">
    Регистрация
  </h2>

  <BulmaNotification type="warning">
    Возможность регистрации пока что не реализована! Следите за обновлениями.
  </BulmaNotification>
</template>