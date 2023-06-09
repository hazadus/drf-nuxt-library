<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';
import { getMediaUrl, fetchBook } from "@/useApi";
import { useBookAdminPageUrl } from "@/urls";
import type { Book } from "@/types";

const authStore = useAuthStore();
const config = useRuntimeConfig();
const route = useRoute();

const book: Ref<Book | null> = ref(null);

const tabName: string = route.params.booksTab as string;
const allowableTabNames = ["details", "notes", "lists",];

if (!allowableTabNames.includes(tabName)) {
  throw createError({
    statusCode: 404,
    message: "Указанный раздел не существует на странице книги!",
    fatal: true,
  });
}

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

  <!-- Breadcrumbs -->
  <nav class="breadcrumb is-small has-arrow-separator" aria-label="breadcrumbs">
    <ul>
      <li>
        <NuxtLink to="/">
          Главная
        </NuxtLink>
      </li>
      <li>
        <NuxtLink to="/books/">
          Все книги
        </NuxtLink>
      </li>
      <li v-if="book" class="is-active">
        <a>
          {{ book.title }}
        </a>
      </li>
    </ul>
  </nav>


  <BulmaNotification type="danger" v-if="bookError">
    <p>
      <b>Ошибка {{ bookError.statusCode }}</b> - попробуйте перезагрузить страницу!
    </p>
    <p>{{ bookError }}</p>
  </BulmaNotification>

  <template v-else-if="book">
    <div class="columns is-vcentered mb-0">
      <div class="column is-10">
        <h2 class="header is-size-2 mb-2" style="line-height: 2.5rem;">
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
            &middot;&nbsp;{{ book.year }} г.
          </span>

          <span v-if="book.pages" class="has-text-grey">
            &middot;&nbsp;{{ book.pages }} с.
          </span>
        </h3>
      </div>

      <div class="column is-2 has-text-centered">
        <!-- "Read" / "Open in admin panel" links -->
        <div v-if="authStore.user?.is_staff || authStore.user?.is_superuser" class="card">
          <footer class="card-footer">
            <NuxtLink v-if="book.file && authStore.user?.is_staff" :to="getMediaUrl(book.file)" class="card-footer-item">
              <Icon name="fa6-solid:book-open-reader" />
            </NuxtLink>
            <a v-if="authStore.user?.is_superuser" :href="useBookAdminPageUrl(book.id as number)" target="_blank"
              class="card-footer-item">
              <Icon name="octicon:tools" />
            </a>
          </footer>
        </div>
      </div>
    </div>

    <div class="columns">
      <div class="column is-10">
        <BulmaTagList class="mb-0 p-0">
          <BulmaTag :tag="tag" v-for="tag in book.tags" :key="`tag-${tag.id}`" />
        </BulmaTagList>

        <!-- Tabs -->
        <div class="tabs is-centered">
          <ul>
            <li :class="tabName === 'details' ? 'is-active' : ''">
              <NuxtLink :to="`/books/${book.id}/details/`">
                <span>
                  <Icon name="mdi:book" />
                </span>
                <span>
                  Сведения
                </span>
              </NuxtLink>
            </li>
            <li :class="tabName === 'notes' ? 'is-active' : ''">
              <NuxtLink :to="`/books/${book.id}/notes/`">
                <span>
                  <Icon name="mdi:notes" />
                </span>
                <span>
                  Заметки
                </span>
              </NuxtLink>
            </li>
            <li :class="tabName === 'lists' ? 'is-active' : ''">
              <NuxtLink :to="`/books/${book.id}/lists/`">
                <span>
                  <Icon name="mdi:format-list-group" />
                </span>
                <span>
                  Списки
                </span>
              </NuxtLink>
            </li>
          </ul>
        </div>

        <!-- Tab content -->
        <BookDetailsTab v-if="tabName == 'details'" :book="book" />
        <BookNotesTab v-else-if="tabName == 'notes'" :bookId="(book.id as number)" />
        <BookListsTab v-else-if="tabName == 'lists'" :bookId="(book.id as number)" />

      </div>

      <div class="column is-2">
        <!-- Book cover -->
        <figure v-if="book.cover_thumbnail_large" class="image is-2by3 mb-2">
          <img :src="getMediaUrl(book.cover_thumbnail_large)">
        </figure>
      </div>
    </div>
  </template>
</template>