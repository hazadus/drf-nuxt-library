<script setup lang="ts">
import type { Book } from '@/types';
import { fetchAllBooks, getMediaUrl } from "@/useApi";

const allBooks: Ref<Book[] | null> = ref(null);

const { data: booksData } = await fetchAllBooks();
allBooks.value = booksData.value;
</script>

<template>
  <Title>
    Последние поступления | Библиотека
  </Title>

  <h2 class="header is-size-2 mb-5">
    Последние поступления
  </h2>

  <div class="box" v-for="book in allBooks" :key="book.id">
    <div class="columns">
      <div class="column is-10">
        <h3 class="header is-size-3">
          <b>{{ book.title }}</b>
        </h3>
        <h4 class="subtitle is-4">
          <template v-for="author in book.authors">
            {{ author.first_name }} {{ author.last_name }}
          </template>

          <span v-if="book.publisher" class="has-text-grey">
            &middot;&nbsp;&laquo;{{ book.publisher.title }}&raquo;
          </span>

          <span v-if="book.year" class="has-text-grey">
            &middot;&nbsp;{{ book.year }}
          </span>
        </h4>

        <BulmaTagList class="mb-3">
          <BulmaTag :tag="tag" v-for="tag in book.tags">
          </BulmaTag>
        </BulmaTagList>

        <NuxtLink :to="`/books/${book.id}/`" class="button is-small">
          Подробнее
        </NuxtLink>
      </div>
      <div class="column is-2">
        <figure v-if="book.cover_image" class="image is-2by3">
          <img :src="getMediaUrl(book.cover_image)">
        </figure>
      </div>
    </div>
  </div>
</template>