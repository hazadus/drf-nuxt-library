<script setup lang="ts">

interface IError {
  statusCode: number
  statusMessage: string
  message: string
}

const props = defineProps({
  // Reference: https://nuxt.com/docs/getting-started/error-handling#rendering-an-error-page 
  error: Object as PropType<IError>,
});

function onClearError() {
  clearError({ redirect: "/" });
}
</script>

<template>
  <Title>
    Ошибка | Библиотека
  </Title>

  <section class="section p-5 page-content-section">
    <div class="container is-widescreen">
      <section class="hero is-small is-warning">
        <div class="hero-body">

          <div class="columns is-vcentered">
            <div class="column is-8">
              <p class="title">
                {{ props.error?.statusCode }}: {{ props.error?.statusMessage }}
              </p>
              <p class="subtitle">
                Извините, произошла ошибка.
              </p>
              <button class="button is-primary" @click="onClearError">
                Вернуться на главную
              </button>
            </div>

            <div class="column is-4">
              <figure class="image">
                <img src="/images/error.png">
              </figure>
            </div>
          </div>

        </div>
      </section>

    </div>
  </section>
</template>

<style>
@import 'bulma/css/bulma.css';

.page-content-section {
  min-height: calc(100vh - 0px - 0px);
}
</style>