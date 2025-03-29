import { createStore } from "vuex";
import router from "@/router";
import { getCookie } from "@/utilities/func";
export default createStore({
  state: {
    user: {
      id: null,
      email: "",
      name: self.name,
      role: "",
      courses: [],
    },
  },
  mutations: {
    set_user(state, user) {
      state.user = user;
    },
    clear_user(state) {
      state.user = {
        id: null,
        email: "",
        name: "",
        role: "",
        courses: [],
      };
    },
  },
  actions: {
    async clearToken({ commit }) {
      localStorage.removeItem("csrf_access_token");
      localStorage.removeItem("csrf_refresh_token");
      commit("clear_user");
    },
    async getToken({ state, commit }) {
      try {
        const csrf_access_token = localStorage.getItem("csrf_access_token");
        if (csrf_access_token) return csrf_access_token;

        const csrf_refresh_token = localStorage.getItem("csrf_refresh_token");
        if (csrf_refresh_token) {
          const response = await fetch("http://localhost:5000/auth/refresh", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRF-TOKEN": csrf_refresh_token,
            },
            credentials: "include",
          });
          const data = await response.json();
          localStorage.setItem(
            "csrf_access_token",
            JSON.stringify(getCookie("csrf_access_token"))
          );
          if (response.ok) return getCookie("csrf_access_token");
        }
        commit("clear_user");
        if (router.currentRoute.value.path === "/Admin") {
          router.replace("/AdminSignIn");
        } else router.replace("/SignIn");
      } catch (error) {
        console.error("Token error: ", error);
      }
    },
    async loadUser({ commit, dispatch }) {
      try {
        const csrf_access_token = await dispatch("getToken");
        if (csrf_access_token) {
          const response = await fetch("http://localhost:5000/user/get", {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "X-CSRF-TOKEN": csrf_access_token,
            },
            credentials: "include",
          });
          const data = await response.json();
          if (response.ok) {
            commit("set_user", data);
            return true;
          } else {
            if (router.currentRoute.value.path === "/Admin") {
              router.replace("/AdminSignIn");} else router.replace("/SignIn");
          }
        }
      } catch (error) {
        console.error("Loading User failed: ", error);
        if (router.currentRoute.value.path === "/Admin") {
          router.replace("/AdminSignIn");} else router.replace("/SignIn");
      }
    },
    async signIn({ commit, dispatch }, payload) {
      try {
        const response = await fetch("http://localhost:5000/auth/signin", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
          body: JSON.stringify({
            email: payload.email,
          }),
        });

        const data = await response.json();
        if (response.ok) {
          const csrf_access_token = getCookie("csrf_access_token");
          const csrf_refresh_token = getCookie("csrf_refresh_token");

          localStorage.setItem(
            "csrf_access_token",
            JSON.stringify(csrf_access_token)
          );
          localStorage.setItem(
            "csrf_refresh_token",
            JSON.stringify(csrf_refresh_token)
          );

          await dispatch("loadUser");

          return true;
        } else if (response.status === 401) {
          return data.error;
        } else {
          router.replace("/SignIn");
        }
      } catch (error) {
        console.error("Sign in failed:", error);
      }
    },
    async signOut({ state, commit, dispatch }) {
      try {
        const csrf_access_token = await dispatch("getToken");
        if (!csrf_access_token) router.replace("/SignIn");
        else {
          const response = await fetch("http://localhost:5000/auth/signout", {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              "X-CSRF-TOKEN": csrf_access_token,
            },
            credentials: "include",
          });

          await dispatch("clearToken");
          if (state.user.id !== null && state.user.role === "admin") {
            router.replace("/AdminSignIn");
          } else {
            router.replace("/SignIn");
          }
        }
      } catch (error) {
        console.error("Signout failed:", error);
      }
    },
  },
});
