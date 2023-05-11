<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';
import { useFormatDateTime } from "@/utils";
import { fetchNotes, createNewNote } from "@/useApi";
import type { Note } from '@/types';

const authStore = useAuthStore();

const props = defineProps({
  bookId: {
    type: Number,
    required: true,
  },
});

const notes: Ref<Note[]> = ref([]);
const newNoteText: Ref<string> = ref("");
const isPosting: Ref<boolean> = ref(false);

const isSubmitDisabled = computed(() => {
  return isPosting.value || newNoteText.value.trim().length < 3 ? true : false;
});

function clearForm() {
  newNoteText.value = "";
}

async function onSubmit() {
  isPosting.value = true;

  const { data: newNoteData } = await createNewNote(props.bookId, newNoteText.value);

  if (newNoteData.value) {
    notes.value.unshift(newNoteData.value);
    clearForm();
  }

  isPosting.value = false;
}

async function fetchData() {
  const { data: notesData } = await fetchNotes(props.bookId);

  if (notesData.value) {
    notes.value = notesData.value;
  }
}

fetchData();
</script>

<template>
  <BulmaNotification v-if="!authStore.isAuthenticated" type="warning">
    Войдите в учетную запись, чтобы создавать примечания к книгам.
  </BulmaNotification>

  <template v-else>
    <form>
      <div class="field">
        <label class="label">Новая заметка</label>
        <div class="control">
          <textarea v-model="newNoteText" :disabled="isPosting" class="textarea"
            placeholder="Напишите заметку к книге. Вы можете использовать разметку Markdown в этом поле."></textarea>
        </div>

        <div v-if="newNoteText.trim().length" class="box mt-3">
          <label class="label">Предварительный просмотр:</label>
          <MarkdownStringRenderer :markdownString="newNoteText" />
        </div>
      </div>

      <div class="field">
        <div class="control has-text-right">
          <button @click.prevent="onSubmit" :disabled="isSubmitDisabled" class="button is-success mr-2"
            :class="isPosting ? 'is-loading' : ''">
            Добавить заметку
          </button>
          <button @click.prevent="clearForm" :disabled="isPosting" class="button is-link is-light">
            Очистить форму
          </button>
        </div>
      </div>
    </form>

    <hr v-if="notes.length">

    <div v-for="note in notes" :key="`note-${note.id}`" class="box">
      <MarkdownStringRenderer :markdownString="note.text" />
      <p class="has-text-grey has-text-right">
        <small>
          Заметка создана {{ useFormatDateTime(note.created) }}
        </small>
      </p>
    </div>
  </template>
</template>