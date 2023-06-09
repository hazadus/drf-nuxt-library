// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiBase: "http://localhost",
    },
  },
  modules: ["@vueuse/nuxt", "nuxt-icon", "@pinia/nuxt", "@nuxt/content"],
  ssr: false,
  app: {
    head: {
      script: [
        {
          src: "https://stats.hazadus.ru/script.js",
          async: true,
          "data-website-id": "958843fa-7e40-42cf-b75e-043dc2ae4480",
        },
      ],
    },
  },
});
