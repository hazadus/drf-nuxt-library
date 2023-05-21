<script setup lang="ts">
import { getMediaUrl } from "@/useApi";
import type { Book } from '@/types';

defineProps({
  book: {
    type: Object as PropType<Book>,
    required: true,
  },
});
</script>

<template>
  <BookCard v-if="false" />

  <div class="content">
    <template v-if="book.description">
      <h5>
        Описание
      </h5>
      <MarkdownStringRenderer :markdownString="book.description" />
    </template>

    <template v-if="book.contents">
      <h5>
        Содержание
      </h5>
      <MarkdownStringRenderer :markdownString="book.contents" />
    </template>
  </div>

  <template v-if="book.authors.length">
    <template v-for="author in book.authors" :key="`author-${author.id}`">
      <template v-if="author.description">
        <hr>
        <div class="box">
          <h5 class="header is-size-5 mb-3">
            {{ author.first_name }} {{ author.last_name }}
          </h5>

          <div class="columns">
            <div class="column is-10">
              <MarkdownStringRenderer :markdownString="author.description" />
            </div>

            <div class="column is-2">
              <figure v-if="author.portrait_thumbnail" class="image is-3by4">
                <img :src="getMediaUrl(author.portrait_thumbnail)">
              </figure>
            </div>
          </div>
        </div>
      </template>
    </template>
  </template>
</template>