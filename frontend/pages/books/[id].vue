<script setup lang="ts">
import { getMediaUrl, fetchBook } from "@/useApi";
import type { Book } from "@/types";
import { useAuthStore } from '@/stores/AuthStore';

const authStore = useAuthStore();
const route = useRoute();

const book: Ref<Book | null> = ref(null);

const { data: bookData, error: bookError } = await fetchBook(route.params.id as string);

if (bookError.value?.statusCode === 404) {
  throw createError({
    statusCode: 404,
    message: `Книга с id = ${route.params.id} не найдена в базе.`,
    fatal: true,
  });
} else if (bookError.value) {
  console.log(bookError.value);
  console.log(bookError.value.statusCode);
} else {
  book.value = bookData.value;
}
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
    <div class="columns is-vcentered">
      <div class="column is-10">
        <h2 class="header is-size-2">
          {{ book.title }}
        </h2>

        <h3 class="subtitle">
          <template v-for="(author, index) in book.authors">
            {{ author.first_name }} {{ author.last_name }}<template v-if="index + 1 < book.authors.length">, </template>
          </template>

          <span v-if="book.publisher" class="has-text-grey">
            &middot;&nbsp;&laquo;{{ book.publisher.title }}&raquo;
          </span>

          <span v-if="book.year" class="has-text-grey">
            &middot;&nbsp;{{ book.year }}
          </span>

          <span v-if="book.pages" class="has-text-grey">
            &middot;&nbsp;{{ book.pages }} с.
          </span>
        </h3>
      </div>

      <div class="column is-2 has-text-centered">
        <NuxtLink v-if="book.file && authStore.user?.is_staff" :to="getMediaUrl(book.file)" class="button is-success">
          Читать
        </NuxtLink>
      </div>
    </div>

    <div class="columns">
      <div class="column is-10">
        <BulmaTagList class="mb-3">
          <BulmaTag :tag="tag" v-for="tag in book.tags">
          </BulmaTag>
        </BulmaTagList>

        <BookCard v-if="false" />

        <BookNotes v-if="false" />

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
            <div class="box" v-if="author.description">
              <div class="columns">
                <div class="column is-10">
                  <h5 class="header is-size-5 mb-3">
                    {{ author.first_name }} {{ author.last_name }}
                  </h5>

                  <MarkdownStringRenderer :markdownString="author.description" />
                </div>

                <div class="column is-2">
                  <figure v-if="author.portrait" class="image is-3by4">
                    <img :src="getMediaUrl(author.portrait)">
                  </figure>
                </div>
              </div>
            </div>
          </template>
        </template>

      </div>

      <div class="column is-2">
        <!-- Book cover -->
        <figure v-if="book.cover_image" class="image is-2by3">
          <img :src="getMediaUrl(book.cover_image)">
        </figure>
      </div>
    </div>
  </template>
</template>