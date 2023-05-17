<template>
  <Title>
    О проекте | Библиотека
  </Title>

  <!-- Breadcrumbs -->
  <nav class="breadcrumb is-small has-arrow-separator" aria-label="breadcrumbs">
    <ul>
      <li>
        <NuxtLink to="/">
          Главная
        </NuxtLink>
      </li>
      <li class="is-active">
        <NuxtLink to="/about/">
          О проекте
        </NuxtLink>
      </li>
    </ul>
  </nav>

  <h2 class="header is-size-2 mb-5">
    О проекте
  </h2>

  <div class="content">
    <p>
      Это веб-приложение, под кодовым названием &laquo;Библиотека&raquo;, предназначено для учета книг в домашней
      библиотеке. Что-то вроде LiveLib или GoodReads, только компактнее, без рекламы и лишней мишуры.
    </p>

    <p>
      Каждый зарегистрированный пользователь может добавлять книги, авторов, издательства, автоматически
      становясь их &laquo;куратором&raquo; с возможностью последующего внесения изменений в информацию о них.
      Добавленные материалы доступны всем пользователям, но каждый может сохранять книги себе, формируя собственную
      библиотеку. К книгам можно добавлять личные заметки и проставлять их статус &mdash; читаю, хочу прочитать, и др.
      Быстрый поиск по сайту позволяет мгновенно найти нужную книгу.
    </p>

    <p>
      Проект находится на стадии активной разработки &mdash; пока ещё мало что работает, но новый функционал добавляется
      каждый день.
    </p>

    <p>
      На чём всё это работает:
      <Icon name="logos:django-icon" /> &middot;
      <Icon name="logos:python" /> &middot;
      <Icon name="logos:gunicorn" /> &middot;
      <Icon name="logos:postgresql" /> &middot;
      <Icon name="logos:nodejs" /> &middot;

      <Icon name="logos:nginx" /> &middot;
      <Icon name="logos:docker-icon" /> &middot;
      <Icon name="logos:ubuntu" /> &middot;
      <Icon name="logos:nuxt-icon" /> &middot;
      <Icon name="logos:vue" /> &middot;
      <Icon name="logos:typescript-icon" /> &middot;
      <Icon name="logos:vueuse" /> &middot;
      <Icon name="logos:bulma" />
    </p>

    <p>
      Исходный код на Github:
      <Icon name="logos:github-octocat" /><a
        href="https://github.com/hazadus/drf-nuxt-library">hazadus/drf-nuxt-library</a>.
    </p>
  </div>
</template>