<script setup lang="ts">
import type { Book } from '@/types';

const route = useRoute();
const config = useRuntimeConfig();

const book: Ref<Book | null> = ref(null);

const { data: bookData, error: bookError } = await useFetch<Book>(() => `${config.public.apiBase}/api/v1/books/${route.params.id}/`, {});

if (bookError.value?.statusCode === 404) {
  throw createError({
    statusCode: 404,
    message: `Книга с id = ${route.params.id} не найдена в базе.`,
    fatal: true,
  });
} else if (bookError.value) {
  console.log(bookError.value);
  console.log(bookError.value.statusCode);
}

book.value = bookData.value;
</script>

<template>
  <Title>
    {{ book ? book.title : "Подробно о книге" }} | Библиотека
  </Title>

  <BulmaNotification type="danger" v-if="bookError">
    <p>
      <b>Ошибка {{ bookError.statusCode }}</b> - попробуйте перезагрузить страницу!
    </p>
    <p>{{ bookError }}</p>
  </BulmaNotification>

  <template v-else-if="book">
    <h2 class="header is-size-2">
      {{ book.title }}
    </h2>
    <h3 class="subtitle">
      <template v-for="(author, index) in book.authors">
        {{ author.first_name }} {{ author.last_name }}<template v-if="index + 1 < book.authors.length">,</template>
      </template>

      <span v-if="book.publisher" class="has-text-grey">
        &middot;&nbsp;&laquo;{{ book.publisher.title }}&raquo;
      </span>

      <span v-if="book.year" class="has-text-grey">
        &middot;&nbsp;{{ book.year }}
      </span>
    </h3>

    <div class="columns">
      <div class="column is-10">
        <BulmaTagList class="mb-3">
          <BulmaTag :tag="tag" v-for="tag in book.tags">
          </BulmaTag>
        </BulmaTagList>

        <BookCard />

        <BookNotes />

        <div class="content">
          <template v-if="book.description">
            <h5>
              Описание
            </h5>
            <p>
              {{ book.description }}
            </p>
          </template>

          <template v-if="book.contents">
            <h5>
              Содержание
            </h5>
            <p>
              {{ book.contents }}
            </p>
          </template>
        </div>

      </div>

      <div class="column is-2">
        <!-- Book cover -->
        <figure v-if="book.cover_image" class="image is-2by3">
          <img :src="`${config.public.apiBase}${book.cover_image}`">
        </figure>
      </div>
    </div>
  </template>
</template>