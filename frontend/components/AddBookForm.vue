<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';
import { fetchAllBooks, fetchAllAuthors, fetchAllPublishers, createNewBook, updateBookFiles } from "@/useApi";
import { useBookDetailsPageUrl } from "@/urls";
import { Book, ListPage, Author, Publisher } from "@/types";

const authStore = useAuthStore();

const availableAuthors: Ref<Author[]> = ref([]);
const availablePublishers: Ref<Publisher[]> = ref([]);

const similarBooks: Ref<Book[]> = ref([]);
const createdBooks: Ref<Book[]> = ref([]);
const fetchErrors: Ref<Object[]> = ref([]);

const titleInputElement: Ref<HTMLInputElement | null> = ref(null);
const coverFileInputElement: Ref<HTMLInputElement | null> = ref(null);
const bookFileInputElement: Ref<HTMLInputElement | null> = ref(null);
const selectedCoverFileName: Ref<string | undefined> = ref(undefined);
const selectedBookFileName: Ref<string | undefined> = ref(undefined);

const title: Ref<string> = ref("");
const selectedAuthorID: Ref<number> = ref(0);
const selectedPublisherID: Ref<number> = ref(0);
const year: Ref<number | undefined> = ref(undefined);
const pages: Ref<number | undefined> = ref(undefined);
const description: Ref<string> = ref("");
const contents: Ref<string> = ref("");

const isFetching: Ref<boolean> = ref(false);
const isPosting: Ref<boolean> = ref(false);


onMounted(() => {
  titleInputElement.value?.focus();
});

const isSubmitDisabled = computed(() => {
  return title.value.trim().length < 3 || selectedAuthorID.value == 0 || isPosting.value ? true : false;
});

const selectedAuthors = computed(() => {
  if (selectedAuthorID.value) {
    return availableAuthors.value.filter((a) => a.id == selectedAuthorID.value);
  } else {
    return [];
  }
});

const selectedPublisher = computed(() => {
  if (selectedPublisherID.value) {
    return availablePublishers.value.filter((p) => p.id == selectedPublisherID.value)[0];
  } else {
    return undefined;
  }
});

watch(title, async () => {
  // Query books by title as user enter new book's title
  const titleTrimmed = title.value.trim();

  if (!isFetching.value && titleTrimmed.length > 2) {
    fetchSimilarBooks();
  } else if (titleTrimmed.length < 3) {
    similarBooks.value = [];
  }
});

function clearForm() {
  title.value = "";
  year.value = undefined;
  pages.value = undefined;
  description.value = "";
  contents.value = "";
}

function onSelectCoverFile() {
  selectedCoverFileName.value = coverFileInputElement.value?.files?.item(0)?.name;
}

function onSelectBookFile() {
  selectedBookFileName.value = bookFileInputElement.value?.files?.item(0)?.name;
}

async function fetchSimilarBooks() {
  isFetching.value = true;
  const { data: booksData } = await fetchAllBooks(1, title.value.trim());
  similarBooks.value = (booksData.value as ListPage<Book>).results;
  isFetching.value = false;
}

async function onSubmit() {
  isPosting.value = true;
  fetchErrors.value = [];

  const newBook: Book = {
    title: title.value,
    authors: selectedAuthors.value,
    publisher: selectedPublisher.value,
    year: year.value,
    pages: pages.value,
    description: description.value,
    contents: contents.value,
  };

  const { data: addedBook, error: postError } = await createNewBook(newBook);

  if (postError.value) {
    fetchErrors.value.push(postError.value.data);
    isPosting.value = false;
    return;
  }

  // Book created - now upload the files:
  if (addedBook.value) {
    let image: File | undefined = undefined;
    let file: File | undefined = undefined;

    if (coverFileInputElement.value?.files?.length) {
      image = coverFileInputElement.value.files.item(0) as File;
    }

    if (bookFileInputElement.value?.files?.length) {
      file = bookFileInputElement.value.files.item(0) as File;
    }

    if (image || file) {
      const { error: updateError } = await updateBookFiles(addedBook.value.id as number, image, file);
      if (updateError.value) fetchErrors.value.push(updateError.value.data);
    }
  }

  if (addedBook.value) createdBooks.value.push(addedBook.value);
  clearForm();
  isPosting.value = false;
}

// Initial fetch
const { data: fetchedAuthors, error: authorsError } = await fetchAllAuthors();
if (authorsError.value) fetchErrors.value.push(authorsError.value.data);
if (fetchedAuthors.value) availableAuthors.value = fetchedAuthors.value;

const { data: fetchedPublishers, error: publishersError } = await fetchAllPublishers();
if (publishersError.value) fetchErrors.value.push(publishersError.value.data);
if (fetchedPublishers.value) availablePublishers.value = fetchedPublishers.value;
</script>

<template>
  <h3 class="header is-size-3 mb-5">
    Добавить книгу
  </h3>

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

  <form enctype="multipart/form-data">
    <div class="field">
      <label class="label">
        Название книги
      </label>
      <div class="control">
        <input v-model="title" ref="titleInputElement" @keyup.escape="title = ''" :disabled="isPosting" class="input"
          type="text" placeholder="Название книги">
      </div>
    </div>

    <BulmaNotification v-if="similarBooks.length" type="warning">
      <div class="icon-text">
        <span class="icon has-text-info is-hidden-mobile">
          <Icon name="mdi:information-variant-circle" />
        </span>
        <span>
          <b>Обратите внимание &mdash; на сайте уже есть книги с похожим названием:</b>
        </span>
      </div>

      <div class="content">
        <ul>
          <li v-for="book in similarBooks" :key="`similar-book-${book.id}`">
            <NuxtLink :to="`/books/${book.id}/`">
              {{ book.title }}
            </NuxtLink>
            <span class="has-text-grey">
              &middot; {{ book.authors[0].first_name }} {{ book.authors[0].last_name }}
            </span>
            <span v-if="book.publisher" class="has-text-grey">
              &middot; &laquo;{{ book.publisher.title }}&raquo;
            </span>
            <span v-if="book.year" class="has-text-grey">
              &middot; {{ book.year }}
            </span>
          </li>
        </ul>
      </div>
    </BulmaNotification>

    <div class="field">
      <label class="label">
        Автор
      </label>
      <div class="control">
        <div class="select">
          <select v-model="selectedAuthorID" :disabled="isPosting">
            <option value="0">
              Выберите автора
            </option>
            <option v-for="author in availableAuthors" :value="author.id" :key="`opt-author-${author.id}`">
              {{ author.last_name }}, {{ author.first_name }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <div class="columns">
      <div class="column is-4">
        <div class="field">
          <label class="label">Издательство</label>
          <div class="control">
            <div class="select">
              <select v-model="selectedPublisherID" :disabled="isPosting">
                <option value="0">
                  Выберите издательство
                </option>
                <option v-for="publisher in availablePublishers" :value="publisher.id" :key="`opt-pub-${publisher.id}`">
                  {{ publisher.title }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <div class="column is-2">
        <div class="field">
          <label class="label">
            Год издания
          </label>
          <div class="control">
            <input v-model="year" :disabled="isPosting" class="input" type="number" placeholder="Год">
          </div>
        </div>
      </div>

      <div class="column is-2">
        <div class="field">
          <label class="label">
            Страниц
          </label>
          <div class="control">
            <input v-model="pages" :disabled="isPosting" class="input" type="number" placeholder="Страниц">
          </div>
        </div>
      </div>

      <div class="column is-4">

      </div>
    </div>

    <div class="columns">
      <div class="column is-6">
        <div class="field">
          <label class="label">
            Обложка
          </label>
          <div class="control">
            <div class="file has-name">
              <label class="file-label">
                <input @change="onSelectCoverFile" :disabled="isPosting" class="file-input" ref="coverFileInputElement"
                  type="file" accept="image/*">
                <span class="file-cta">
                  <span class="file-icon">
                    <Icon name="mdi:file-image" />
                  </span>
                  <span class="file-label">
                    Выберите изображение
                  </span>
                </span>
                <span class="file-name">
                  {{ selectedCoverFileName }}
                </span>
              </label>
            </div>
          </div>
        </div>
      </div>

      <div class="column is-6">
        <div v-if="authStore.user?.is_staff" class="field">
          <label class="label">
            Файл книги
          </label>
          <div class="control">
            <div class="file has-name">
              <label class="file-label">
                <input @change="onSelectBookFile" :disabled="isPosting" class="file-input" ref="bookFileInputElement"
                  type="file">
                <span class="file-cta">
                  <span class="file-icon">
                    <Icon name="mdi:file-pdf" />
                  </span>
                  <span class="file-label">
                    Выберите файл книги
                  </span>
                </span>
                <span class="file-name">
                  {{ selectedBookFileName }}
                </span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="field">
      <label class="label">Описание</label>
      <div class="control">
        <textarea v-model="description" :disabled="isPosting" class="textarea"
          placeholder="Краткое описание издания"></textarea>
      </div>
      <div class="box mt-3" v-if="description.length">
        <MarkdownStringRenderer :markdownString="description" />
      </div>
    </div>

    <div class="field">
      <label class="label">Содержание</label>
      <div class="control">
        <textarea v-model="contents" :disabled="isPosting" class="textarea"
          placeholder="Произведения или главы, включенные в издание"></textarea>
      </div>
      <div class="box mt-3" v-if="contents.length">
        <MarkdownStringRenderer :markdownString="contents" />
      </div>
    </div>

    <!-- Select tags for new book -->
    <div v-if="false" class="columns">
      <div class="column is-6">
        <div class="field">
          <label class="label">Выбранные метки:</label>
          <div class="control">

          </div>
        </div>
      </div>

      <div class="column is-6">
        <div class="field">
          <label class="label">Доступные метки:</label>
          <div class="control">

          </div>
        </div>
      </div>
    </div>

    <div class="field is-grouped">
      <div class="control">
        <button @click.prevent="onSubmit" :disabled="isSubmitDisabled" class="button is-link"
          :class="isPosting ? 'is-loading' : ''">
          Добавить книгу
        </button>
      </div>
      <div class="control">
        <button @click.prevent="clearForm" :disabled="isPosting" class="button is-link is-light">
          Очистить форму
        </button>
      </div>
    </div>
  </form>

  <BulmaNotification v-if="createdBooks.length" type="success" class="mt-3">
    <div class="content">
      <p>
        <b>Вы добавили книги:</b>
      </p>
      <ul>
        <li v-for="book in createdBooks" :key="`created-book-${book.id}`">
          <NuxtLink :to="useBookDetailsPageUrl(book.id as number)">
            {{ book.title }}
          </NuxtLink>
          <span v-if="book.year" class="has-text-grey">
            &middot; {{ book.year }}
          </span>
        </li>
      </ul>
      <p>
        Спасибо за участие в развитии проекта!
      </p>
    </div>
  </BulmaNotification>
</template>