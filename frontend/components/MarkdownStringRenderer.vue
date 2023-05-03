<script setup>
// Reference: https://stackoverflow.com/a/67054151/20197519

import markdownParser from "@nuxt/content/transformers/markdown"

const props = defineProps({
  markdownString: {
    type: String,
    required: true,
  }
});

const record = ref("");

watchEffect(async () => {
  await markdownParser.parse("custom.md", props.markdownString).then((md) => record.value = md);
});
</script>

<template>
  <div class="content">
    <ContentRendererMarkdown :value="record" v-if="record" />
  </div>
</template>