<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';
import { getMediaUrl, fetchBookList } from "@/useApi";
import { useBookDetailsPageUrl, useBookListAdminPageUrl } from "@/urls";
import { useFormatDateTime } from "@/utils";
import type { BookList } from "@/types";

const authStore = useAuthStore();
const route = useRoute();

const list: Ref<BookList | undefined> = ref(undefined);
const errors: Ref<Object[]> = ref([]);

const totalPagesInList = computed(() => {
  let totalPages = 0;
  if (list.value) {
    list.value.items.forEach(item => {
      totalPages += item.book.pages || 0;
    });
  }
  return totalPages;
});

const { data: listData, error: listFetchErrors } = await fetchBookList(route.params.id as string);

if (listFetchErrors.value) errors.value.push(listFetchErrors.value);
if (listData.value) list.value = listData.value;
</script>

<template>
  <!-- Breadcrumbs -->
  <nav class="breadcrumb is-small has-arrow-separator" aria-label="breadcrumbs">
    <ul>
      <li>
        <NuxtLink to="/">
          Главная
        </NuxtLink>
      </li>
      <li>
        <NuxtLink to="/lists/">
          Списки книг
        </NuxtLink>
      </li>
      <li class="is-active">
        <a href="#" aria-current="page">
          {{ list?.title }}
        </a>
      </li>
    </ul>
  </nav>

  <ErrorListNotification v-if="errors.length" :errors="errors" />

  <template v-if="list">
    <Title>
      {{ list.title }} | Библиотека
    </Title>

    <h2 class="header is-size-2">
      {{ list.title }}
    </h2>

    <div class="content">
      <p class="has-text-grey">
        Книг в списке – {{ list.items.length }}
        &middot;&nbsp;Всего страниц – {{ totalPagesInList }}
        &middot;&nbsp;Создан <b>{{ list.user.username }}</b>
        &middot;&nbsp;{{ useFormatDateTime(list.created) }}
        <template v-if="authStore.user?.is_superuser">
          &middot;&nbsp;<a :href="useBookListAdminPageUrl(list.id)" target="_blank">Править в админке</a>
        </template>
      </p>
    </div>

    <MarkdownStringRenderer v-if="list.description" :markdownString="list.description" class="mb-6" />

    <article v-for="item in list.items" :key="`item-${item.id}`" class="media">
      <figure v-if="item.book.cover_thumbnail_medium" class="media-left">
        <p class="image is-64x64">
          <NuxtLink :to="useBookDetailsPageUrl(item.book.id as number)">
            <img :src="getMediaUrl(item.book.cover_thumbnail_medium)">
          </NuxtLink>
        </p>
      </figure>
      <div class="media-content">
        <div class="content">
          <NuxtLink :to="useBookDetailsPageUrl(item.book.id as number)">
            <h5 class="header is-size-5">
              {{ item.book.title }}
            </h5>
          </NuxtLink>

          <MarkdownStringRenderer v-if="item.description" class="mb-5" :markdownString="item.description" />

          <BulmaNotification v-if="item.book.description">
            <h6 class="header is-size-6">
              О книге
            </h6>
            <MarkdownStringRenderer :markdownString="item.book.description" />
          </BulmaNotification>
        </div>
      </div>
    </article>
  </template>
</template>