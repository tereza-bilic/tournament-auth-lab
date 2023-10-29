<template>
  <suspense>
    <template #default>
      <div>
        <q-toolbar class="bg-grey-3">
          <q-toolbar-title class="text-weight-medium">
            {{name}}
            <q-badge color="positive" align="top" style="margin-right: 2px;" :label="winScore ?? 0" />
            <q-badge color="info" align="top" style="margin-right: 2px;" :label="tieScore ?? 0" />
            <q-badge color="negative" align="top" :label="loseScore ?? 0" />
          </q-toolbar-title>

          <template v-for="participant in participants">
            <q-chip outline color="bg-gray-9" text-color="white">{{participant}}</q-chip>
          </template>
        </q-toolbar>

        <q-page>
          <div class="game">
            <MatchEditor :matches="matches" :isEditable="isEditable" :updateMatch="updateMatch"/>
            <LeaderBoard :matches="matches" :participants="participants" :win="winScore" :lose="loseScore" :tie="tieScore"/>
          </div>
        </q-page>
      </div>
    </template>

    <template #fallback>
      <q-spinner-gears size="100px" color="primary" />
    </template>
  </suspense>
</template>

<style>
  .game {
    display: flex;
    justify-content: space-evenly;
  }
</style>

<script setup lang="ts">
  import LeaderBoard from '../components/LeaderBoard.vue'
  import MatchEditor from '../components/MatchEditor.vue'
  import { useAuth0 } from '@auth0/auth0-vue';
  import { useRoute } from 'vue-router'
  import { computed, reactive, ref } from 'vue'
  import env_config from '../../env_config.json'
  import axios from 'axios'

  const auth0 = useAuth0();
  const route = useRoute();
  const { id } = route.params;

  const name = ref(null)
  const participants = ref(null)
  const winScore = ref(null)
  const tieScore = ref(null)
  const loseScore = ref(null)
  const gameData = await axios.get(`${env_config.api}/games/${id}`)

  const isEditable = computed(() => {
    return auth0.isAuthenticated.value && !auth0.isLoading.value && auth0.user.value?.sub === gameData.data.creator
  });


  name.value = gameData.data.name,
  participants.value = gameData.data.participants.split(','),
  winScore.value = gameData.data.winScore,
  tieScore.value = gameData.data.tieScore,
  loseScore.value = gameData.data.loseScore
  const matches = reactive(gameData.data.matches)

  const updateMatch = async(match: {id: number}, newScore: string) => {
    await axios.patch(`${env_config.api}/matches/${match.id}`, {
      score: newScore
    });

    console.log(matches)

    if (!matches) {
      return;
    }

    const matchIndex = matches.findIndex((m: any) => m.id === match.id);
    console.log(matchIndex)
    matches[matchIndex].score = newScore
  }
</script>
