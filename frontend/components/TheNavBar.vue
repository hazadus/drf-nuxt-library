<script setup lang="ts">

const route = useRoute();

const showMobileMenu: Ref<boolean> = ref(false);
</script>

<template>
  <nav class="navbar has-shadow is-light">
    <div class="container is-widescreen">

      <!-- Site title -->
      <div class="navbar-brand">
        <NuxtLink to="/" class="navbar-item">
          <h2 class="title is-size-3">
            Библиотека
          </h2>
        </NuxtLink>
        <div class="navbar-burger burger" @click="showMobileMenu = !showMobileMenu">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>

      <div class="navbar-menu" :class="showMobileMenu ? 'is-active' : ''">
        <div class="navbar-start">
          <!-- Menu items -->
          <NuxtLink to="/books/" class="navbar-item" :class="route.path === '/books/' ? 'is-active' : ''"
            @click="showMobileMenu = false">
            Все книги
          </NuxtLink>
          <NuxtLink to="/add-book/" class="navbar-item" :class="route.path.startsWith('/add-') ? 'is-active' : ''"
            @click="showMobileMenu = false">
            Добавить
          </NuxtLink>
          <NuxtLink to="/about/" class="navbar-item" :class="route.path === '/about/' ? 'is-active' : ''"
            @click="showMobileMenu = false">
            О проекте
          </NuxtLink>
        </div>

        <div class="navbar-end">
          <!-- Buttons -->
          <div class="navbar-item">
            <div class="buttons">
              <NuxtLink to="/signup/" class="button is-primary" @click="showMobileMenu = false">
                <strong>
                  Регистрация
                </strong>
              </NuxtLink>
              <NuxtLink to="/login/" class="button" @click="showMobileMenu = false">
                Войти
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>