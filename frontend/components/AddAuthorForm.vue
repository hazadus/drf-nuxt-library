<script setup lang="ts">
import { Author } from "@/types";
import { fetchAllAuthors, createNewAuthor, getMediaUrl } from "@/useApi";

const existingAuthors: Ref<Author[]> = ref([]);
const createdAuthors: Ref<Author[]> = ref([]);
const fetchErrors: Ref<Object[]> = ref([]);

const lastNameInputElement: Ref<HTMLInputElement | null> = ref(null);
const fileInputElement: Ref<HTMLInputElement | null> = ref(null);
const selectedFileName: Ref<string | undefined> = ref(undefined);
const isPosting: Ref<boolean> = ref(false);

const firstName: Ref<string> = ref("");
const middleName: Ref<string> = ref("");
const lastName: Ref<string> = ref("");
const description: Ref<string> = ref("");

const similarAuthors = computed(() => {
  // Check if there's already authors with similar last name.
  if (lastName.value.trim().length < 3) {
    return [];
  }

  return existingAuthors.value.filter((author) => {
    return author.last_name.toLowerCase().includes(
      lastName.value.trim().toLowerCase()
    )
  });
});

const isSubmitDisabled = computed(() => {
  return lastName.value.trim().length < 3 || isPosting.value;
});

onMounted(() => {
  lastNameInputElement.value?.focus();
});

function clearForm() {
  lastName.value = "";
  firstName.value = "";
  middleName.value = "";
  description.value = "";
  if (fileInputElement.value) {
    fileInputElement.value.value;
  }
}

function onSelectFile() {
  selectedFileName.value = fileInputElement.value?.files?.item(0)?.name;
}

async function onSubmit() {
  isPosting.value = true;
  fetchErrors.value = [];

  const formData = new FormData();
  formData.append("first_name", firstName.value);
  formData.append("middle_name", middleName.value);
  formData.append("last_name", lastName.value);
  formData.append("description", description.value);

  const { data: addedAuthor, error: postError } = await createNewAuthor(formData);

  if (postError.value) {
    fetchErrors.value.push(postError.value.data);
  }

  if (addedAuthor.value) {
    createdAuthors.value.push(addedAuthor.value);
    existingAuthors.value.push(addedAuthor.value);
    clearForm();
  }

  isPosting.value = false;
}

// Do the initial data fetch
const { data: fetchedAuthors } = await fetchAllAuthors();
existingAuthors.value = fetchedAuthors.value || [];
</script>

<template>
  <h3 class="header is-size-3 mb-5">
    Добавить автора
  </h3>

  <BulmaNotification v-if="fetchErrors.length" type="danger">
    <div class="content">
      <div class="icon-text mb-3">
        <span class="icon has-text-warning is-hidden-mobile">
          <Icon name="mdi:exclamation" />
        </span>
        <span>
          <b>При добавлении автора произошла ошибка!</b>
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

  <form>
    <div class="field">
      <label class="label">
        Фамилия
      </label>
      <div class="control">
        <input v-model="lastName" ref="lastNameInputElement" :disabled="isPosting" class="input" type="text"
          placeholder="Фамилия автора - обязательное поле">
      </div>
    </div>

    <BulmaNotification v-if="similarAuthors.length" type="warning">
      <div class="content">
        <div class="icon-text">
          <span class="icon has-text-info is-hidden-mobile">
            <Icon name="mdi:information-variant-circle" />
          </span>
          <span>
            <b>Обратите внимание &mdash; на сайте уже есть похожие авторы:</b>
          </span>
        </div>
        <ul>
          <li v-for="author in similarAuthors" :key="`similar-author-${author.id}`">
            {{ author.first_name }} {{ author.last_name }}
          </li>
        </ul>
      </div>
    </BulmaNotification>

    <div class="field">
      <label class="label">
        Имя
      </label>
      <div class="control">
        <input v-model="firstName" :disabled="isPosting" class="input" type="text" placeholder="Имя автора">
      </div>
    </div>

    <div class="field">
      <label class="label">
        Отчество
      </label>
      <div class="control">
        <input v-model="middleName" :disabled="isPosting" class="input" type="text" placeholder="Отчество автора">
      </div>
    </div>

    <div class="field">
      <label class="label">Сведения об авторе</label>
      <div class="control">
        <textarea v-model="description" :disabled="isPosting" class="textarea"
          placeholder="Информация об авторе. Вы можете использовать разметку Markdown в этом поле."></textarea>
      </div>
      <div v-if="description.trim().length" class="box mt-3">
        <label class="label">Предварительный просмотр:</label>
        <MarkdownStringRenderer :markdownString="description" />
      </div>
    </div>

    <div class="field">
      <label class="label">
        Портрет автора
      </label>
      <div class="control">
        <div class="file has-name">
          <label class="file-label">
            <input @change="onSelectFile" :disabled="isPosting" class="file-input" ref="fileInputElement" type="file"
              accept="image/*">
            <span class="file-cta">
              <span class="file-icon">
                <Icon name="mdi:file-upload-outline" />
              </span>
              <span class="file-label">
                Выберите файл с изображением
              </span>
            </span>
            <span class="file-name">
              {{ selectedFileName }}
            </span>
          </label>
        </div>
      </div>
    </div>

    <div class="field is-grouped">
      <div class="control">
        <button @click.prevent="onSubmit" :disabled="isSubmitDisabled" class="button is-link">
          Добавить автора
        </button>
      </div>
      <div class="control">
        <button @click.prevent="clearForm" :disabled="isPosting" class="button is-link is-light">
          Очистить форму
        </button>
      </div>
    </div>
  </form>

  <BulmaNotification v-if="createdAuthors.length" type="light" class="mt-3">
    <div class="content">
      <p>
        <b>Вы добавили авторов:</b>
      </p>

      <article v-for="author in createdAuthors" :key="`created-author-${author.id}`" class="media">
        <figure v-if="author.portrait" class="media-left">
          <p class="image is-64x64">
            <img :src="getMediaUrl(author.portrait)">
          </p>
        </figure>
        <div class="media-content">
          <div class="content">
            <p>
              <strong>
                {{ author.first_name }} {{ author.middle_name }} {{ author.last_name }}
              </strong>
            </p>
            <MarkdownStringRenderer v-if="author.description" :markdownString="author.description" />
          </div>
        </div>
      </article>

      <p>
        Спасибо за участие в развитии проекта!
      </p>
    </div>
  </BulmaNotification>
</template>