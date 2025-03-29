<template>
  <router-view  :key="$route.fullPath"></router-view>
</template>

<script>

import { mapActions } from 'vuex';
import { mapState } from 'vuex';
export default {
  methods: {
    ...mapActions(['loadUser'])
  },
  computed: {
    ...mapState(['user'])
  },
  async created(){
    await this.loadUser();   
},
}
</script>

<style>
@import url("../src/assets/style.css");
</style>