<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';
import { getMediaUrl } from "@/useApi";
import { useFormatDateTime } from "@/utils";

definePageMeta({
  middleware: "auth",
});

const authStore = useAuthStore();
</script>

<template>
  <Title>
    {{ authStore.user?.username }} | Библиотека
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
        <NuxtLink to="/profile/">
          Ваш профиль
        </NuxtLink>
      </li>
    </ul>
  </nav>

  <h2 class="header is-size-2 mb-5">
    Ваш профиль
  </h2>

  <div class="columns">
    <div class="column is-6" :key="authStore.user?.id">
      <table class="table">
        <tbody>
          <tr>
            <td>
              Имя пользователя:
            </td>
            <td>{{ authStore.user?.username }}</td>
          </tr>
          <tr>
            <td>
              Имя:
            </td>
            <td>{{ authStore.user?.first_name }}</td>
          </tr>
          <tr>
            <td>
              Фамилия:
            </td>
            <td>{{ authStore.user?.last_name }}</td>
          </tr>
          <tr>
            <td>
              E-mail:
            </td>
            <td>{{ authStore.user?.email }}</td>
          </tr>
          <tr>
            <td>
              Зарегистрирован:
            </td>
            <td>
              <template v-if="authStore.user">
                {{ useFormatDateTime(authStore.user.date_joined) }}
              </template>
            </td>
          </tr>
          <tr>
            <td>
              Последний вход:
            </td>
            <td>
              <template v-if="authStore.user">
                {{ useFormatDateTime(authStore.user?.last_login) }}
              </template>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="column is-6">
      <figure v-if="authStore.user?.profile_image_thumbnail_large" class="image is-1by1">
        <img class="is-rounded" :src="getMediaUrl(authStore.user.profile_image_thumbnail_large)"
          style="width: 300px; height: 300px;">
      </figure>
    </div>
  </div>
</template>