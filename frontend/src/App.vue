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
  }
}
</script>

<style>
@import url("../src/assets/style.css");
</style>