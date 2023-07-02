<script setup lang="ts">
import { fetchBookListsWithBook } from "@/useApi";
import { useBookListDetailPageUrl } from "@/urls";
import type { BookList } from '@/types';

const props = defineProps({
  bookId: {
    type: Number,
    required: true,
  },
});

const lists: Ref<BookList[]> = ref([]);
const isFetching: Ref<boolean> = ref(false);
const fetchErrors: Ref<Object[]> = ref([]);

async function fetchData() {
  isFetching.value = true;
  const { data: listsData, error: fetchListsError } = await fetchBookListsWithBook(props.bookId);

  if (fetchListsError.value) {
    fetchErrors.value.push(fetchListsError.value.data);
  }

  if (listsData.value) {
    lists.value = listsData.value;
  }

  isFetching.value = false;
}

fetchData();
</script>

<template>
  <BulmaNotification v-if="fetchErrors.length" type="danger">
    <div class="content">
      <div class="icon-text mb-3">
        <span class="icon has-text-warning is-hidden-mobile">
          <Icon name="mdi:exclamation" />
        </span>
        <span>
          <b>При обращении к серверу произошла ошибка!</b>
        </span>
      </div>
      <ul>
        <template v-for="error in fetchErrors">
          <li v-for="value, key in error">
            {{ key }}: {{ value }}
          </li>
        </template>
      </ul>
    </div>
  </BulmaNotification>

  <h4 class="is-size-4 mb-2">
    Книга входит в списки:
  </h4>

  <template v-if="!isFetching">
    <template v-if="lists.length">
      <div class="card mb-2" v-for="list in lists" :key="`list-${list.id}`">
        <header class="card-header">
          <p class="card-header-title">
            {{ list.title }}
          </p>
        </header>
        <div class="card-content">
          <div class="content">
            {{ list.description }}
          </div>
        </div>
        <footer class="card-footer">
          <a :href="useBookListDetailPageUrl(list.id)" class="card-footer-item">
            Открыть
          </a>
          <span class="card-footer-item">
            <template v-if="list.is_public">
              <Icon name="ic:baseline-public" />
            </template>
            <template v-else>
              <Icon name="ic:baseline-public-off" />
            </template>
            &middot;{{ list.items.length }}&nbsp;
            <Icon name="noto:books" />
          </span>
          <span class="card-footer-item">
            <Icon name="ic:baseline-person" />
            {{ list.user.username }}
          </span>
        </footer>
      </div>
    </template>
    <BulmaNotification v-else type="warning">
      Пока нет списков, содержащих данную книгу.
    </BulmaNotification>
  </template>
</template>