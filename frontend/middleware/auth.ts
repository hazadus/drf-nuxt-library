import { useAuthStore } from "@/stores/AuthStore";

const authStore = useAuthStore();

// Reference: https://nuxt.com/docs/getting-started/routing#route-middleware
export default defineNuxtRouteMiddleware((to, from) => {
  // Init the store, because middleware somehow called before the store is initialized in App.vue.
  authStore.initializeStore();
  if (!authStore.isAuthenticated) {
    return navigateTo('/login/')
  }
});