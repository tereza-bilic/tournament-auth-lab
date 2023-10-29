<script setup lang="ts">
import { RouterLink } from 'vue-router'
import SignupButton from '../components/SignupButton.vue'
import LogoutButton from '@/components/LogoutButton.vue';
import { useAuth0 } from '@auth0/auth0-vue';

const { isAuthenticated } = useAuth0();
</script>

<template>
  <template v-if="!isAuthenticated">
    <signup-button />
  </template>

  <template v-if="isAuthenticated">
    <router-link to="/new-game">Create a new game</router-link>
    <logout-button />
  </template>
</template>
