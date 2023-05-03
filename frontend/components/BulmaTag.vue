<script setup lang="ts">
// https://bulma.io/documentation/elements/tag/

import type { Tag } from '@/types';

// https://vuejs.org/guide/typescript/composition-api.html#typing-component-props
// Note absence of angle brackets below, and `type: Object as PropType<Tag>` stuff:
const props = defineProps({
  tag: {
    type: Object as PropType<Tag>,
    required: true,
  },
  type: {
    type: String,
    default: "info",
    required: false,
  },
  isLight: {
    type: Boolean,
    default: true,
    required: false,
  },
  hasDeleteButton: Boolean,
  hasCounter: {
    type: Boolean,
    default: false,
    required: false,
  }
});

const emit = defineEmits<{
  (e: "clickTag", tag: Tag): void;
  (e: "delete", tag: Tag): void;
}>();

function onClickTag() {
  emit("clickTag", props.tag);
}

function onClickDelete() {
  emit("delete", props.tag);
}
</script>

<template>
  <div class="control">
    <div class="tags has-addons">
      <a :class="`tag is-${props.type} ${isLight ? 'is-light' : ''}`" @click="onClickTag">
        {{ tag.title }}
      </a>
      <a class="tag is-delete" v-if="props.hasDeleteButton" @click="onClickDelete"></a>
      <a class="tag" v-else v-if="hasCounter">
        0
      </a>
    </div>
  </div>
</template>