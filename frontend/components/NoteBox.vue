<script setup lang="ts">
import { deleteNote, updateNote } from "@/useApi";
import { useFormatDateTime } from "@/utils";
import type { Note } from '@/types';

const props = defineProps({
  note: {
    type: Object as PropType<Note>,
    required: true,
  },
});

const emit = defineEmits<{
  (e: "updated", note: Note): void;
  (e: "deleted", note: Note): void;
}>();

const updatedNoteText: Ref<string> = ref("");
const isEditing: Ref<boolean> = ref(false);
const isPosting: Ref<boolean> = ref(false);

const isSubmitDisabled = computed(() => {
  return isPosting.value || updatedNoteText.value.trim().length < 3 ? true : false;
});

function onClickEdit() {
  updatedNoteText.value = props.note.text;
  isEditing.value = true;
}

async function onClickDelete() {
  let isConfirmed = confirm("Вы уверены, что хотите удалить заметку?");

  if (!isConfirmed) {
    return;
  }

  const { error: deleteError } = await deleteNote(props.note.id as number);

  if (deleteError.value) {
    console.error("Error deleting note.");
    console.log(deleteError.value);
  } else {
    emit("deleted", props.note);
  }
}

async function onSubmitEdit() {
  isPosting.value = true;

  const { data: updatedNote, error: updateError } = await updateNote(props.note.id as number, updatedNoteText.value);

  if (updateError.value) {
    console.error("Error updating note!");
    console.log(updateError.value);
    isPosting.value = false;
  } else {
    emit("updated", updatedNote.value as Note);
    isPosting.value = false;
    isEditing.value = false;
  }
}
</script>

<template>
  <div class="box">
    <template v-if="!isEditing">
      <MarkdownStringRenderer :markdownString="note.text" />
      <p class="has-text-grey has-text-right">
        <small>
          Заметка создана {{ useFormatDateTime(note.created) }}
          &middot;&nbsp;<a @click.prevent="onClickEdit">Править</a>
          &middot;&nbsp;<a @click.prevent="onClickDelete">Удалить</a>
        </small>
      </p>
    </template>

    <template v-else>
      <form>
        <div class="field">
          <label class="label">Отредактируйте заметку:</label>
          <div class="control">
            <textarea v-model="updatedNoteText" :disabled="isPosting" class="textarea"
              placeholder="Отредактируйте заметку к книге. Вы можете использовать разметку Markdown в этом поле."></textarea>
          </div>

          <div v-if="updatedNoteText.trim().length">
            <hr>
            <label class="label">Предварительный просмотр:</label>
            <MarkdownStringRenderer :markdownString="updatedNoteText" />
            <hr>
          </div>
        </div>

        <div class="field">
          <div class="control has-text-right">
            <button @click.prevent="onSubmitEdit" class="button is-success mr-2" :disabled="isSubmitDisabled"
              :class="isPosting ? 'is-loading' : ''">
              Сохранить
            </button>
            <button @click.prevent="isEditing = false" :disabled="isPosting" class="button is-link is-light">
              Отмена
            </button>
          </div>
        </div>
      </form>
    </template>
  </div>
</template>