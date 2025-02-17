import { createStore } from "vuex";
import router from "@/router";
export default createStore({
  state: {
    user: null,
    cgpa:null,
    projectCgpa:null
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
      state.cgpa = user.cgpa;
      state.projectCgpa = user.projectCgpa;
    },
  },
  actions: {
    signIn({ commit }) {
      setTimeout(() => {
        const userData = { name: "Example Student", email: "student@example.com", cgpa:9, projectCgpa:10, selectedCourses:[]};
        commit("setUser", userData);
        router.push("/Dashboard");

      }, 1000);
    },
  },
});
