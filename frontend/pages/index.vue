<template>
  <Title>
    Добро пожаловать! | Библиотека
  </Title>

  <!-- Breadcrumbs -->
  <nav class="breadcrumb is-small has-arrow-separator" aria-label="breadcrumbs">
    <ul>
      <li class="is-active">
        <NuxtLink to="/">
          Главная
        </NuxtLink>
      </li>
    </ul>
  </nav>

  <section class="hero is-medium is-info">
    <div class="hero-body">
      <div class="columns is-vcentered">
        <div class="column is-7">
          <p class="title">
            Добро пожаловать в библиотеку!
          </p>
          <p class="subtitle">
            Добавляйте книги, составляйте списки, пишите заметки &mdash; читать книги ещё никогда не было так
            увлекательно!
          </p>
        </div>

        <div class="column is-5">
          <figure class="image">
            <img src="/images/matrixlibrary.jpg">
          </figure>
        </div>
      </div>
    </div>
  </section>
</template>