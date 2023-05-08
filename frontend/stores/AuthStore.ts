import { defineStore } from "pinia";
import type { User } from "@/types";

interface StateShape {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
}

export const useAuthStore = defineStore("AuthStore", {
  state: (): StateShape => ({
    token: null,
    user: null,
    isAuthenticated: false,
  }),
  getters: {},
  actions: {
    initializeStore() {
      if (localStorage.getItem("drf-nuxt-library-token")) {
        this.token = localStorage.getItem("drf-nuxt-library-token");
        this.isAuthenticated = true;
      } else {
        this.token = null;
        this.isAuthenticated = false;
      }

      const userInfo = localStorage.getItem("drf-nuxt-library-user");
      if (userInfo) {
        this.user = JSON.parse(userInfo);
      } else {
        localStorage.setItem(
          "drf-nuxt-library-user",
          JSON.stringify(this.user),
        );
      }
    },
    setUser(user: User | null) {
      this.user = user;
      localStorage.setItem("drf-nuxt-library-user", JSON.stringify(this.user));
    },
    logIn(token: string, user: User) {
      this.token = token;
      this.isAuthenticated = true;
      this.setUser(user);
      localStorage.setItem("drf-nuxt-library-token", this.token);
    },
    logOut() {
      this.token = "";
      this.isAuthenticated = false;
      this.setUser(null);
      localStorage.setItem("drf-nuxt-library-token", this.token);
    },
  },
});
