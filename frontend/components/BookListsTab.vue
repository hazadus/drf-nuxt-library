<script setup lang="ts">
import { fetchBookListsWithBook, fetchOnlyOwnBookLists, createNewListItem, deleteListItem } from "@/useApi";
import { useAuthStore } from "@/stores/AuthStore";
import { useBookListDetailPageUrl } from "@/urls";
import type { BookList, BookListItem } from '@/types';

const props = defineProps({
  bookId: {
    type: Number,
    required: true,
  },
});

const authStore = useAuthStore();
const lists: Ref<BookList[]> = ref([]);
const usersOwnLists: Ref<BookList[]> = ref([]);
const isFetching: Ref<boolean> = ref(false);
const isPosting: Ref<boolean> = ref(false);
const isDeleting: Ref<boolean> = ref(false);
const fetchErrors: Ref<Object[]> = ref([]);
const selectedListID: Ref<number> = ref(0);

const usersOwnListsWithoutTheBook = computed(() => {
  // Exclude lists already containing the book:
  return usersOwnLists.value.filter((list) => {
    return list.items.filter((listItem) => listItem.book.id == props.bookId).length == 0;
  });
});

const isSubmitDisabled = computed(() => {
  return isFetching.value || isPosting.value || isDeleting.value || selectedListID.value == 0;
});

const isRemoveBookButtonDisabled = computed(() => {
  return isFetching.value || isPosting.value || isDeleting.value;
});

async function fetchData() {
  isFetching.value = true;

  const { data: listsData, error: fetchListsError } = await fetchBookListsWithBook(props.bookId);
  if (fetchListsError.value) fetchErrors.value.push(fetchListsError.value.data);
  if (listsData.value) lists.value = listsData.value;

  if (authStore.isAuthenticated) {
    // Fetch authenticated user's public and private lists:
    const { data: usersOwnListsData, error: fetchUsersOwnListsError } = await fetchOnlyOwnBookLists();
    if (fetchUsersOwnListsError.value) fetchErrors.value.push(fetchUsersOwnListsError.value.data);
    if (usersOwnListsData.value) usersOwnLists.value = usersOwnListsData.value;
  }

  isFetching.value = false;
}

async function onSubmit() {
  isPosting.value = true;

  const { error: postError } = await createNewListItem(props.bookId, selectedListID.value);

  if (postError.value) {
    fetchErrors.value.push(postError.value.data);
    isPosting.value = false;
    return;
  }

  await fetchData();
  selectedListID.value = 0;
  isPosting.value = false;
}

async function onClickRemoveBookFromList(listToDeleteFrom: BookList) {
  // Find corresponding `ListItem`:
  const listItem: BookListItem | undefined = listToDeleteFrom.items.find((item) => item.book.id == props.bookId);

  if (listItem) {
    isDeleting.value = true;

    const { error: deleteErrors } = await deleteListItem(listItem.id);

    if (deleteErrors.value) {
      fetchErrors.value.push(deleteErrors.value);
      isDeleting.value = false;
      return;
    }

    await fetchData();
    isDeleting.value = false;
  }
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

  <template v-if="lists">
    <template v-if="lists.length">
      <div class="card mb-2" v-for="list in lists" :key="`list-${list.id}`">
        <header class="card-header">
          <p class="card-header-title">
            {{ list.title }}
          </p>
          <div class="buttons" v-if="authStore.user?.id == list.user.id">
            <button class="button is-warning mr-2" @click.prevent="onClickRemoveBookFromList(list)"
              :disabled="isRemoveBookButtonDisabled">
              <span class="mr-4">
                <Icon name="tabler:book-off" />
              </span>
              <span>
                Убрать
              </span>
            </button>
          </div>
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
    <template v-else>
      <BulmaNotification v-if="!isFetching" type="warning">
        Пока нет списков, содержащих данную книгу.
      </BulmaNotification>
    </template>
  </template>

  <template v-if="authStore.isAuthenticated">
    <hr>

    <h4 class="is-size-4 mb-2">
      Добавить книгу в список
    </h4>

    <div v-if="usersOwnListsWithoutTheBook.length" class="field">
      <label class="label">Список книг</label>
      <div class="control">
        <div class="select mr-2">
          <select v-model="selectedListID" :disabled="isPosting">
            <option value="0">
              Выберите список
            </option>
            <option v-for="list in usersOwnListsWithoutTheBook" :value="list.id" :key="`opt-own-list-${list.id}`">
              {{ list.title }}
            </option>
          </select>
        </div>
        <button @click.prevent="onSubmit" :disabled="isSubmitDisabled" class="button is-link"
          :class="isPosting ? 'is-loading' : ''">
          Добавить книгу
        </button>
      </div>
    </div>
    <template v-else>
      <BulmaNotification v-if="!isFetching" type="warning">
        Нет списков, в которые вы можете добавить данную книгу.
      </BulmaNotification>
    </template>
  </template>
</template>