<script setup lang="ts">
import type { Book, ListPage } from '@/types';
import { fetchAllBooks } from "@/useApi";

const router = useRouter();

const booksListPage: Ref<ListPage<Book> | null> = ref(null);
let totalBooksCount: number = 0;

const searchInputElement: Ref<HTMLInputElement | null> = ref(null);
const searchQuery: Ref<string> = ref("");
const isFetching: Ref<boolean> = ref(false);

// Get first page of the Book list and total Book count
await fetchBookListPageNumber(1);
if (booksListPage.value) {
  totalBooksCount = booksListPage.value.count;
}

onMounted(() => {
  searchInputElement.value?.focus();
});

watch(searchQuery, async () => {
  if (!isFetching.value) {
    doSearch();
  }
});

async function doSearch() {
  // Request first page of the Book list, filtered by `searchQuery`.
  fetchBookListPageNumber(1);
}

async function fetchBookListPageNumber(page: number) {
  // Request required page of the Book list, filtered by `searchQuery`.
  let query: string | undefined = searchQuery.value.trim();
  query = query.length >= 3 ? query : undefined;

  isFetching.value = true;
  const { data: booksData } = await fetchAllBooks(page, query);
  booksListPage.value = booksData.value;
  isFetching.value = false;
}

function onPressEnter() {
  if (booksListPage.value?.results.length) {
    router.push(`/books/${booksListPage.value.results[0].id}/details/`);
  }
}
</script>

<template>
  <Title>
    Все книги | Библиотека
  </Title>

  <!-- Breadcrumbs -->
  <nav class="breadcrumb is-small has-arrow-separator" aria-label="breadcrumbs">
    <ul>
      <li>
        <NuxtLink to="/">
          Главная
        </NuxtLink>
      </li>
      <li class="is-active">
        <NuxtLink to="/books/">
          Все книги
        </NuxtLink>
      </li>
    </ul>
  </nav>

  <!-- Search query input  -->
  <div class="field">
    <div class="control has-icons-left is-large" :class="isFetching ? 'is-loading' : ''">
      <input ref="searchInputElement" v-model="searchQuery" @keyup.enter="onPressEnter" @keyup.escape="searchQuery = ''"
        class="input is-large" type="text" placeholder="Печатайте для поиска по всем книгам...">
      <span class="icon is-left">
        <Icon name="mdi:search" />
      </span>
    </div>
  </div>

  <!-- Search results summary -->
  <nav class="level is-mobile">
    <div class="level-item has-text-centered">
      <div>
        <p class="heading">
          Всего книг
        </p>
        <p class="title">
          {{ totalBooksCount }}
        </p>
      </div>
    </div>
    <div class="level-item has-text-centered">
      <div>
        <p class="heading">
          Найдено по запросу
        </p>
        <p class="title">
          {{ booksListPage?.count || 0 }}
        </p>
      </div>
    </div>
    <div v-if="false" class="level-item has-text-centered">
      <div>
        <p class="heading">
          Найдено в ваших книгах
        </p>
        <p class="title">
          ?
        </p>
      </div>
    </div>
  </nav>

  <!-- Book list items -->
  <BookListItem v-if="booksListPage?.results.length" v-for="book in booksListPage?.results" :book="book"
    :key="`book-${book.id}`" />
  <BulmaNotification v-else>
    <p>Не найдено книг, соответствующих вашему запросу.</p>
    <p>Вы можете <NuxtLink to="/add-book/">добавить новую книгу</NuxtLink> самостоятельно!</p>
  </BulmaNotification>


  <!-- Bottom pagination -->
  <nav v-if="booksListPage?.count" class="pagination" role="navigation" aria-label="pagination">
    <a @click="fetchBookListPageNumber(booksListPage.page - 1)" class="pagination-previous"
      :class="booksListPage?.previous ? '' : 'is-disabled'">
      Назад
    </a>
    <a @click="fetchBookListPageNumber(booksListPage.page + 1)" class="pagination-next"
      :class="booksListPage.next ? '' : 'is-disabled'">
      Вперёд
    </a>
    <ul class="pagination-list">
      <li v-for="pageNumber in booksListPage.total_pages">
        <a @click="fetchBookListPageNumber(pageNumber)" class="pagination-link"
          :class="pageNumber == booksListPage.page ? 'is-current' : ''" aria-label="Goto page">
          {{ pageNumber }}
        </a>
      </li>
    </ul>
  </nav>
</template>