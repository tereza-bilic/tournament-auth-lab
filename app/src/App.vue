<script setup lang="ts">
  import { RouterLink, RouterView } from 'vue-router'
  import Error from './components/Error.vue'

</script>

<template>
  <error />
  <suspense>
    <template #default>
      <router-view />
    </template>

    <template #fallback>
      <q-spinner-gears size="100px" color="primary" />
    </template>
  </suspense>
</template>


<style scoped>
</style>
