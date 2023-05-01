<script setup lang="ts">
import type { Book } from '@/types';

const config = useRuntimeConfig();

const allBooks: Ref<Book[] | null> = ref(null);

async function fetchAllBooks() {
  const { data: books, error: booksError } = await useFetch<Book[]>(() => `${config.public.apiBase}/api/v1/books/`, {});

  allBooks.value = books.value as Book[];
}

onBeforeMount(() => {
  fetchAllBooks();
});
</script>

<template>
  <Title>
    Последние поступления | Библиотека
  </Title>

  <h2 class="header is-size-2 mb-5">
    Последние поступления
  </h2>

  <div class="box" v-for="book in allBooks" :key="(book as Book).id">
    <div class="columns">
      <div class="column is-10">
        <h3 class="header is-size-3">
          <b>{{ (book as Book).title }}</b>
        </h3>
        <h4 class="subtitle is-4">
          <template v-for="author in (book as Book).authors">
            {{ author.first_name }} {{ author.last_name }}
          </template>
        </h4>

        <NuxtLink :to="`/books/${(book as Book).id}/`" class="button is-small">
          Подробнее
        </NuxtLink>
      </div>
      <div class="column is-2">
        <figure v-if="(book as Book).cover_image" class="image is-2by3">
          <img :src="`${config.public.apiBase}${(book as Book).cover_image}`">
        </figure>
      </div>
    </div>
  </div>
</template>