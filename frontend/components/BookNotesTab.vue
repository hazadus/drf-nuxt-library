<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';
import { useFormatDateTime } from "@/utils";
import { fetchNotes } from "@/useApi";
import type { Note } from '@/types';

const authStore = useAuthStore();

const props = defineProps({
  bookId: {
    type: Number,
    required: true,
  },
});

const notes: Ref<Note[]> = ref([]);

const { data: notesData } = await fetchNotes(props.bookId);

if (notesData.value) {
  notes.value = notesData.value;
}

</script>

<template>
  <BulmaNotification v-if="!authStore.isAuthenticated" type="warning">
    Войдите в учетную запись, чтобы создавать примечания к книгам.
  </BulmaNotification>

  <template v-else>
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