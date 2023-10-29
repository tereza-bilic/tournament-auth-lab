<script setup lang="ts">
  import { RouterLink, RouterView } from 'vue-router'
  import Error from './components/Error.vue'


</script>

<template>
  <error />
  <suspense>
    <template #default>
      <q-layout
        view="lhh LpR lff"
        container
        style="height: 100vh"
        class="bg-grey-9 shadow"
      >
        <q-header reveal class="dark">
          <q-toolbar>
              <q-btn flat round dense icon="map" to="/"/>
              <q-toolbar-title>Tournament Manager</q-toolbar-title>
            </q-toolbar>
        </q-header>

        <q-page-container>
          <router-view />
        </q-page-container>
      </q-layout>
    </template>

    <template #fallback>
      <q-spinner-gears size="100px" color="primary" />
    </template>
  </suspense>
</template>


<style scoped>
</style>
