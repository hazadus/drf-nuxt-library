<script setup lang="ts">
import type { BookList } from '@/types';
import { fetchAllLists, getMediaUrl } from "@/useApi";
import { useAuthStore } from '@/stores/AuthStore';

const authStore = useAuthStore();
const config = useRuntimeConfig();

const lists: Ref<BookList[]> = ref([]);

const { data: listsData } = await fetchAllLists();

if (listsData.value) {
  lists.value = listsData.value;
}
</script>

<template>
  <Title>
    Списки книг | Библиотека
  </Title>

  <h3 class="header is-size-3 mb-5">
    Списки книг
  </h3>

  <template v-if="lists.length">
    <div v-for="list in lists" :key="`booklist-${list.id}`" class="box mb-3">
      <h4 class="header is-size-4">
        <a>
          {{ list.title }}
        </a>
      </h4>
      <h5 class="subtitle has-text-grey">
        {{ list.items.length }} книг
        <span v-if="list.is_public">
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
          <li v-if="item.book.cover_image" class="list-item">
            <figure>
              <p class="image is-2x3">
                <a :href="`/books/${item.book.id}/details/`">
                  <img :src="getMediaUrl(item.book.cover_image)" :alt="item.book.title">
                </a>
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
            <a :href="`${config.public.apiBase}/admin/books/list/${list.id}/change/`" target="_blank">
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