<template>
  <button class="button__sign-up" @click="handleSignUp">Sign Up</button>
</template>

<script lang="ts" setup>
import { useAuth0 } from "@auth0/auth0-vue";

const { loginWithRedirect } = useAuth0();

const handleSignUp = () => {
  loginWithRedirect({
    appState: {
      target: "/",
    },
    authorizationParams: {
      screen_hint: "signup",
    }
  });
};
</script>
