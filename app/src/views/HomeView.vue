<script setup lang="ts">
import { RouterLink } from 'vue-router'
import SignupButton from '../components/SignupButton.vue'
import LogoutButton from '@/components/LogoutButton.vue';
import { useAuth0 } from '@auth0/auth0-vue';

const { isAuthenticated, isLoading } = useAuth0();
</script>

<template>
  <template v-if="isLoading">
    <q-spinner color="primary" size="3em"/>
  </template>
  <template v-else>
    <template v-if="!isAuthenticated">
      <q-banner rounded style="margin: 10rem">
        <span class="text-body2">Welcome to Tournament Manager! To create a new game you need to sign in. If you want to view an existing game, please ask the game creator to send you the link.</span>

        <template v-slot:action>
          <signup-button />
        </template>
      </q-banner>
    </template>

    <template v-if="isAuthenticated">
      <logout-button style="float: inline-end;"/>
      <q-banner rounded style="margin: 10rem">

        <span class="text-body2">Welcome to Tournament Manager! You can create a new game here. If you want to view an existing game, please ask the game creator to send you the link.</span>

        <template v-slot:action>
          <q-btn to="/new-game" flat rounded color="primary"  label="Create tournament"/>
        </template>
      </q-banner>
    </template>
  </template>
</template>
