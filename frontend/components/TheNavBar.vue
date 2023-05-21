<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';
import { getMediaUrl } from "@/useApi";

const authStore = useAuthStore();
const route = useRoute();
const router = useRouter();

const showMobileMenu: Ref<boolean> = ref(false);

async function onClickLogOut() {
  /*
    Delete auth data from local storage.
    Forward user to login page.
  */
  showMobileMenu.value = false;
  authStore.logOut();
  router.push("/login/");
}
</script>

<template>
  <nav class="navbar has-shadow is-light">
    <div class="container is-widescreen">

      <!-- Site title -->
      <div class="navbar-brand">
        <NuxtLink to="/" class="navbar-item">
          <Icon name="mdi:library" class="has-text-link" />&nbsp;
          <h3 class="title is-size-3">
            Библиотека
          </h3>
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
            <Icon name="mdi:bookshelf" />&nbsp;
            Все книги
          </NuxtLink>
          <NuxtLink to="/lists/" class="navbar-item" :class="route.path === '/lists/' ? 'is-active' : ''"
            @click="showMobileMenu = false">
            <Icon name="mdi:format-list-group" />&nbsp;
            Списки
          </NuxtLink>
          <NuxtLink to="/add-book/" class="navbar-item" :class="route.path.startsWith('/add-') ? 'is-active' : ''"
            @click="showMobileMenu = false">
            <Icon name="mdi:file-plus-outline" />&nbsp;
            Добавить
          </NuxtLink>
          <NuxtLink to="/about/" class="navbar-item" :class="route.path === '/about/' ? 'is-active' : ''"
            @click="showMobileMenu = false">
            О проекте
          </NuxtLink>
        </div>

        <div class="navbar-end">
          <!-- Buttons -->
          <div class="navbar-item" v-if="!authStore.isAuthenticated">
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

          <!-- Profile drop-down -->
          <div class="navbar-item has-dropdown is-hoverable" v-if="authStore.isAuthenticated && authStore.user">
            <div class="navbar-link user-menu">
              <figure v-if="authStore.user.profile_image_thumbnail_small"
                class="image mr-2 is-hidden-mobile is-hidden-tablet-only">
                <img class="is-rounded is-32x32 "
                  style="width: 32px !important; height: 32px !important; max-height: 32px !important;"
                  :src="getMediaUrl(authStore.user.profile_image_thumbnail_small)">
              </figure>
              {{ authStore.user.username }}
            </div>
            <!-- NB: `key` added to re-render menu (thus, hide dropdown) on each route change. -->
            <div class="navbar-dropdown is-right" :key="route.path">
              <NuxtLink to="/profile/" class="navbar-item" @click="showMobileMenu = false">
                <span class="icon-text">
                  <span class="icon">
                    <Icon name="mdi:book-account" />
                  </span>
                  <span>
                    Профиль
                  </span>
                </span>
              </NuxtLink>
              <NuxtLink to="/books/" class="navbar-item" @click="showMobileMenu = false">
                <span class="icon-text">
                  <span class="icon">
                    <Icon name="material-symbols:folder-managed-rounded" />
                  </span>
                  <span>
                    Книги
                  </span>
                </span>
              </NuxtLink>
              <a class="navbar-item" @click="onClickLogOut()">
                <span class="icon-text">
                  <span class="icon">
                    <Icon name="mdi:logout" />
                  </span>
                  <span>
                    Выйти
                  </span>
                </span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.user-menu {
  min-width: 200px;
}
</style>