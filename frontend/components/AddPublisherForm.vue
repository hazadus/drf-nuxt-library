<script setup lang="ts">
import { Publisher } from "@/types";
import { fetchAllPublishers, createNewPublisher } from "@/useApi";

const existingPublishers: Ref<Publisher[]> = ref([]);
const createdPublishers: Ref<Publisher[]> = ref([]);
const fetchErrors: Ref<Object[]> = ref([]);

const titleInputElement: Ref<HTMLInputElement | null> = ref(null);
const isPosting: Ref<boolean> = ref(false);
const newPublisherTitle: Ref<string> = ref("");

const similarPublishers = computed(() => {
  // Check if there's already publishers with similar titles.
  if (newPublisherTitle.value.trim().length < 3) {
    return [];
  }

  return existingPublishers.value.filter((pub) => {
    return pub.title.toLowerCase().includes(
      newPublisherTitle.value.trim().toLowerCase()
    )
  });
});

const isSubmitDisabled = computed(() => {
  return similarPublishers.value.length || newPublisherTitle.value.trim().length < 3 || isPosting.value ? true : false;
});

onMounted(() => {
  titleInputElement.value?.focus();
});

async function onSubmit() {
  isPosting.value = true;
  fetchErrors.value = [];

  const { data: addedPublisher, error: postError } = await createNewPublisher(newPublisherTitle.value);

  if (postError.value) {
    fetchErrors.value.push(postError.value.data);
  }

  if (addedPublisher.value) {
    createdPublishers.value.push(addedPublisher.value);
    existingPublishers.value.push(addedPublisher.value);
    newPublisherTitle.value = "";
  }

  isPosting.value = false;
}

const { data: fetchedPublishers } = await fetchAllPublishers();
existingPublishers.value = fetchedPublishers.value || [];
</script>

<template>
  <h3 class="header is-size-3 mb-5">
    Добавить издательство
  </h3>

  <BulmaNotification v-if="fetchErrors.length" type="danger">
    <div class="content">
      <div class="icon-text mb-3">
        <span class="icon has-text-warning is-hidden-mobile">
          <Icon name="mdi:exclamation" />
        </span>
        <span>
          <b>При добавлении издательства произошла ошибка!</b>
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
        Название
      </label>
      <div class="control">
        <input ref="titleInputElement" v-model="newPublisherTitle" :disabled="isPosting" class="input" type="text"
          placeholder="Название издательства">
      </div>
    </div>

    <BulmaNotification v-if="similarPublishers.length" type="warning">
      <div class="content">
        <div class="icon-text">
          <span class="icon has-text-info is-hidden-mobile">
            <Icon name="mdi:information-variant-circle" />
          </span>
          <span>
            <b>Обратите внимание &mdash; на сайте уже есть издательства с похожим названием:</b>
          </span>
        </div>
        <ul>
          <li v-for="publisher in similarPublishers" :key="`similar-publishers-${publisher.id}`">
            {{ publisher.title }}
          </li>
        </ul>
      </div>
    </BulmaNotification>

    <div class="field is-grouped">
      <div class="control">
        <button :disabled="isSubmitDisabled" @click.prevent="onSubmit" class="button is-link"
          :class="isPosting ? 'is-loading' : ''">
          Добавить издательство
        </button>
      </div>
      <div class="control">
        <button @click.prevent="newPublisherTitle = ''" :disabled="isPosting" class="button is-link is-light">
          Очистить форму
        </button>
      </div>
    </div>
  </form>

  <BulmaNotification v-if="createdPublishers.length" type="success" class="mt-3">
    <div class="content">
      <p>
        <b>Вы добавили издательства:</b>
      </p>
      <ul>
        <li v-for=" publisher  in  createdPublishers " :key="`created-publisher-${publisher.id}`">
          {{ publisher.title }}
        </li>
      </ul>
      <p>
        Спасибо за участие в развитии проекта!
      </p>
    </div>
  </BulmaNotification>
</template>