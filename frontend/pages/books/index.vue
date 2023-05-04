<script setup lang="ts">
import type { Book } from '@/types';
import { fetchAllBooks, getMediaUrl } from "@/useApi";

const allBooks: Ref<Book[] | null> = ref(null);
const searchInputElement: Ref<HTMLInputElement | null> = ref(null);
const searchQuery: Ref<String> = ref("");

const { data: booksData } = await fetchAllBooks();
allBooks.value = booksData.value;

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

  <!-- Content -->
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