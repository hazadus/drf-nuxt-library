// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    runtimeConfig: {
        public: {
          apiBase: "http://127.0.0.1:8000",
        },
      },
        modules: [
        "@vueuse/nuxt",
        "nuxt-icon",
        "@pinia/nuxt",
    ],
    ssr: false,
})
