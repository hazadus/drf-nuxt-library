<script setup lang="ts"></script>

<template>
  <Title> Регистрация | Библиотека </Title>

  <!-- Breadcrumbs -->
  <nav class="breadcrumb is-small has-arrow-separator" aria-label="breadcrumbs">
    <ul>
      <li>
        <NuxtLink to="/"> Главная </NuxtLink>
      </li>
      <li class="is-active">
        <NuxtLink to="/signup/"> Регистрация </NuxtLink>
      </li>
    </ul>
  </nav>

  <h2 class="header is-size-2 mb-5">Регистрация</h2>

  <BulmaNotification type="warning">
    В настоящий момент работа над проектом приостановлена, поэтому
    зарегистрироваться нет возможности.
  </BulmaNotification>
</template>
