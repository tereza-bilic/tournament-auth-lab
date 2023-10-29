<template>
  <suspense>
    <template #default>
      <div>
          <div class="text-h4">{{ name }} </div>
          <div class="game">
            <MatchEditor :matches="matches" :isEditable="isEditable" :updateMatch="updateMatch"/>
            <LeaderBoard :matches="matches" :participants="participants" :win="winScore" :lose="loseScore" :tie="tieScore"/>
          </div>
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
  }
</style>

<script setup lang="ts">
  import LeaderBoard from '../components/LeaderBoard.vue'
  import MatchEditor from '../components/MatchEditor.vue'
  import { useAuth0 } from '@auth0/auth0-vue';
  import { useRoute } from 'vue-router'
  import { reactive, ref } from 'vue'
  import axios from 'axios'

  const auth0 = useAuth0();
  const route = useRoute();
  const { id } = route.params;

  const name = ref(null)
  const participants = ref(null)
  const winScore = ref(null)
  const tieScore = ref(null)
  const loseScore = ref(null)
  const gameData = await axios.get(`http://127.0.0.1:5000/games/${id}`)

  const isEditable = auth0.isAuthenticated && auth0.user.value?.sub === gameData.data.creator;


  name.value = gameData.data.name,
  participants.value = gameData.data.participants.split(','),
  winScore.value = gameData.data.winScore,
  tieScore.value = gameData.data.tieScore,
  loseScore.value = gameData.data.loseScore
  const matches = reactive(gameData.data.matches)

  const updateMatch = async(match: {id: number}, newScore: string) => {
    await axios.patch(`http://127.0.0.1:5000/matches/${match.id}`, {
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
