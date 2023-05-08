// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiBase: "http://localhost",
    },
  },
  modules: ["@vueuse/nuxt", "nuxt-icon", "@pinia/nuxt", "@nuxt/content"],
  ssr: false,
});
