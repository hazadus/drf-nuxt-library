import { ru } from "@formkit/i18n";
import { defineFormKitConfig } from "@formkit/vue";
import { createProPlugin, inputs } from "@formkit/pro";

export default defineFormKitConfig(() => {
  const config = useRuntimeConfig();
  const pro = createProPlugin(config.formKitProKey, inputs);

  return {
    plugins: [pro],
    locales: { ru },
    locale: "ru",
  };
});
