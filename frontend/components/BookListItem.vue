<script setup lang="ts">
/*
* Component represents one item in the Book list.
*/
import { useAuthStore } from '@/stores/AuthStore';
import { getMediaUrl } from "@/useApi";
import { useBookDetailsPageUrl, useBookNotesPageUrl } from "@/urls";
import type { Book } from '@/types';

const authStore = useAuthStore();

defineProps({
  book: {
    type: Object as PropType<Book>,
    required: true,
  },
});
</script>

<template>
  <div class="box">
    <div class="columns">
      <div class="column is-10">
        <h3 class="header is-size-3">
          <NuxtLink :to="useBookDetailsPageUrl(book.id as number)">
            {{ book.title }}
          </NuxtLink>
        </h3>
        <h4 class="subtitle is-4">
          <template v-for="(author, index) in book.authors">
            {{ author.first_name }} {{ author.last_name }}<template v-if="index + 1 < book.authors.length">, </template>
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

        <template v-if="book.file && authStore.user?.is_staff">
          <NuxtLink :to="getMediaUrl(book.file)" class="button is-small mr-2">
            Читать
          </NuxtLink>
        </template>

        <NuxtLink v-if="authStore.isAuthenticated" :to="useBookNotesPageUrl(book.id as number)"
          class="button is-small mr-2">
          Заметки
        </NuxtLink>

        <NuxtLink :to="useBookDetailsPageUrl(book.id as number)" class="button is-small">
          Сведения
        </NuxtLink>
      </div>
      <div class="column is-2">
        <figure v-if="book.cover_image" class="image is-2by3">
          <NuxtLink :to="useBookDetailsPageUrl(book.id as number)">
            <img :src="getMediaUrl(book.cover_image)">
          </NuxtLink>
        </figure>
      </div>
    </div>
  </div>
</template>