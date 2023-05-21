<script setup lang="ts">
import type { BookList } from '@/types';
import { fetchAllBookLists, getMediaUrl } from "@/useApi";
import { useAuthStore } from '@/stores/AuthStore';
import { useBookDetailsPageUrl, useBookListDetailPageUrl, useBookListAdminPageUrl } from "@/urls";

const authStore = useAuthStore();

const lists: Ref<BookList[]> = ref([]);
const errors: Ref<Object[]> = ref([]);

const { data: listsData, error: listFetchErrors } = await fetchAllBookLists();

if (listFetchErrors.value) errors.value.push(listFetchErrors.value);
if (listsData.value) lists.value = listsData.value;
</script>

<template>
  <Title>
    Списки книг | Библиотека
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
        <NuxtLink to="/lists/">
          Списки книг
        </NuxtLink>
      </li>
    </ul>
  </nav>

  <h3 class="header is-size-3 mb-5">
    Списки книг
  </h3>

  <ErrorListNotification v-if="errors.length" :errors="errors" />

  <template v-if="lists.length">
    <div v-for="list in lists" :key="`booklist-${list.id}`" class="box mb-3">
      <h4 class="header is-size-4">
        <NuxtLink :to="useBookListDetailPageUrl(list.id)">
          {{ list.title }}
        </NuxtLink>
      </h4>
      <h5 class="subtitle has-text-grey">
        {{ list.items.length }} книг
        <span v-if="list.is_public">
          &middot;&nbsp;Составил <b>{{ list.user.username }}</b>
          &middot;&nbsp;
          <Icon name="ic:baseline-public" />
        </span>
        <span v-else>
          &middot;&nbsp;
          <Icon name="ic:baseline-public-off" />
        </span>
      </h5>

      <!-- Book covers -->
      <ul class="book-cover-list">
        <template v-for="item in list.items" :key="`book-item-${item.book.id}`">
          <li v-if="item.book.cover_thumbnail_small" class="list-item">
            <figure>
              <p class="image is-2x3">
                <NuxtLink :to="useBookDetailsPageUrl(item.book.id as number)">
                  <img :src="getMediaUrl(item.book.cover_thumbnail_small)" :alt="item.book.title">
                </NuxtLink>
              </p>
            </figure>
          </li>
        </template>
      </ul>

      <!-- Admin links -->
      <template v-if="authStore.user?.is_superuser">
        <hr class="my-2">
        <p class="has-text-right">
          <small>
            <a :href="useBookListAdminPageUrl(list.id)" target="_blank">
              В админке
            </a>
          </small>
        </p>
      </template>
    </div>
  </template>
</template>

<style scoped>
.book-cover-list {
  display: flex;
  flex-wrap: wrap;
}

.list-item {
  width: 64px;
  margin: 2px;
  flex-shrink: 0;
}
</style>