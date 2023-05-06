<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';
import type { User } from "@/types";

const config = useRuntimeConfig();
const authStore = useAuthStore();
const router = useRouter();

const usernameInputElement: Ref<HTMLInputElement | null> = ref(null);
const username: Ref<string> = ref("");
const password: Ref<string> = ref("");
const fetchErrors: Ref<Object[]> = ref([]);

const isFetching: Ref<boolean> = ref(false);

interface AuthToken {
  auth_token: string;
}

async function submitForm() {
  fetchErrors.value = [];
  isFetching.value = true;

  const formData = {
    username: username.value,
    password: password.value,
  };

  const { data: authData, error: loginError } = await useFetch(() => `${config.public.apiBase}/api/v1/token/login/`, {
    method: "POST", body: formData,
  });

  if (loginError.value) {
    fetchErrors.value.push(loginError.value.data);
    isFetching.value = false;
    return;
  }

  const token = authData.value as AuthToken;

  // Fetch user info
  const { data: userData, error: userDataError } = await useFetch(() => `${config.public.apiBase}/api/v1/user/details/`, {
    headers: [
      ["Authorization", "Token " + token.auth_token,],
    ]
  });

  if (userDataError.value) {
    fetchErrors.value.push(userDataError.value.data);
    isFetching.value = false;
    return;
  }

  const user = userData.value as User;

  // Save token and user info in store:
  authStore.logIn(token.auth_token, user);

  isFetching.value = false;

  // Forward user to the bookmark list
  router.push("/books/");
}

onMounted(() => {
  usernameInputElement.value?.focus();
});

onBeforeMount(() => {
  if (authStore.isAuthenticated) {
    router.push("/books/");
  }
});
</script>

<template>
  <Title>
    Вход в учетную запись | Библиотека
  </Title>

  <div class="columns">
    <div class="column is-6 is-offset-3">
      <div class="box">
        <h1 class="title is-size-2  ">
          Войти
        </h1>
        <h2 class="subtitle">
          Зайдите на сайт со своей учетной записью
        </h2>
        <form @submit.prevent="submitForm">
          <div class="field">
            <label>
              Пользователь:
            </label>
            <div class="control">
              <input v-model="username" ref="usernameInputElement" :disabled="isFetching" type="text" class="input"
                id="username" />
            </div>
          </div>

          <div class="field">
            <label>
              Пароль:
            </label>
            <div class="control">
              <input v-model="password" :disabled="isFetching" type="password" class="input" id="password" />
            </div>
          </div>

          <BulmaNotification v-if="fetchErrors.length" type="danger">
            <div class="content">
              <div class="icon-text mb-3">
                <span class="icon has-text-warning is-hidden-mobile">
                  <Icon name="mdi:exclamation" />
                </span>
                <span>
                  <b>При обращении к серверу произошла ошибка!</b>
                </span>
              </div>
              <ul>
                <template v-for="error in fetchErrors">
                  <li v-for="value, key in error">
                    {{ key }}: {{ value }}
                  </li>
                </template>
              </ul>
            </div>
          </BulmaNotification>

          <div class="field">
            <div class="control has-text-right">
              <button :disabled="isFetching" class="button is-success" :class="isFetching ? 'is-loading' : ''">
                Войти
              </button>
            </div>
          </div>

          <hr />

          <p class="mb-3">
            <NuxtLink to="/signup/" class="is-link">Зарегистрируйтесь</NuxtLink>,
            если у вас ещё нет учетной записи.
          </p>
        </form>
      </div>
    </div>
  </div>
</template>