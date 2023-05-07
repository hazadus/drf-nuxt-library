<script setup lang="ts">
definePageMeta({
  middleware: "auth",
});

const route = useRoute();

const asset: string = route.params.asset as string;
const allowableAssets = ["book", "author", "publisher", "tag",];

if (!allowableAssets.includes(asset)) {
  throw createError({
    statusCode: 404,
    message: "Указанный раздел не существует на странице 'Добавить материал'!"
  });
}
</script>

<template>
  <Title>
    Добавить материалы | Библиотека
  </Title>

  <!-- Tabs -->
  <div class="tabs is-centered">
    <ul>
      <li :class="asset === 'book' ? 'is-active' : ''">
        <NuxtLink to="/add-book/">
          <span>
            <Icon name="mdi:book-plus" />
          </span>
          <span>
            Книга
          </span>
        </NuxtLink>
      </li>
      <li :class="asset === 'author' ? 'is-active' : ''">
        <NuxtLink to="/add-author/">
          <span>
            <Icon name="mdi:badge-account-horizontal-outline" />
          </span>
          <span>
            Автор
          </span>
        </NuxtLink>
      </li>
      <li :class="asset === 'publisher' ? 'is-active' : ''">
        <NuxtLink to="/add-publisher/">
          <span>
            <Icon name="mdi:bookshelf" />
          </span>
          <span>
            Издательство
          </span>
        </NuxtLink>
      </li>
      <li :class="asset === 'tag' ? 'is-active' : ''">
        <NuxtLink to="/add-tag/">
          <span>
            <Icon name="mdi:tag-plus-outline" />
          </span>
          <span>
            Метка
          </span>
        </NuxtLink>
      </li>
    </ul>
  </div>

  <!-- Tab content -->
  <AddBookForm v-if="asset === 'book'" />
  <AddAuthorForm v-else-if="asset === 'author'" />
  <AddPublisherForm v-else-if="asset === 'publisher'" />
  <AddTagForm v-else-if="asset === 'tag'" />
</template>