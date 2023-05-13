<script setup lang="ts">
import { deleteNote } from "@/useApi";
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
</script>

<template>
  <div class="box">
    <MarkdownStringRenderer :markdownString="note.text" />
    <p class="has-text-grey has-text-right">
      <small>
        Заметка создана {{ useFormatDateTime(note.created) }}
        &middot;&nbsp;<a>Править</a>
        &middot;&nbsp;<a @click.prevent="onClickDelete">Удалить</a>
      </small>
    </p>
  </div>
</template>