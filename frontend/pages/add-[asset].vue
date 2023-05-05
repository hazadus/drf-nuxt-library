<script setup lang="ts">
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

  <!-- Page content -->
  <!-- Add book -->
  <AddBookForm v-if="asset === 'book'" />

  <template v-else-if="asset === 'author'">
    <h3 class="header is-size-3">
      Добавить автора
    </h3>
  </template>

  <AddPublisherForm v-else-if="asset === 'publisher'" />

  <template v-else-if="asset === 'tag'">
    <h3 class="header is-size-3">
      Добавить метку
    </h3>
  </template>
</template>