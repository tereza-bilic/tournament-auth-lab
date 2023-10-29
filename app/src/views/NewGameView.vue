<template>
  <div class="view">
    <div class="q-pa-md form">
      <q-form
        @submit="onSubmit"
        @reset="onReset"
        class="q-gutter-md"
      >
        <q-input
          filled
          v-model="name"
          label="Game name *"
          lazy-rules
          :rules="[ val => val && val.length > 0 || 'Please type something']"
        />

        <q-input
          filled
          type="text"
          v-model="participants"
          label="Participants"
          lazy-rules
          :rules="[
            val => val !== null && val !== '' || 'Please type a number of participants',
          ]"
        />

        <div class="scoring">
          <q-input
            filled
            type="number"
            v-model="winScore"
            label="Win score"
            lazy-rules
            :rules="[
              val => val !== null && val !== '' || 'Please type a win score',
            ]"
          />

          <q-input
            filled
            type="number"
            v-model="tieScore"
            label="Tie score"
            lazy-rules
            :rules="[
              val => val !== null && val !== '' || 'Please type a tie score',
            ]"
          />

          <q-input
            filled
            type="number"
            v-model="loseScore"
            label="Lose score"
            lazy-rules
            :rules="[
              val => val !== null && val !== '' || 'Please type a lose score',
            ]"
          />
      </div>


        <div>
          <q-btn label="Submit" type="submit" color="primary"/>
          <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
        </div>
      </q-form>
    </div>
    </div>
</template>

<style>
  .form {
    width: 500px;
    margin: 0 auto;
    margin-top: 10rem;
  }

  .view {
    height: 100vh;
    width: 100vw;
  }

  .scoring {
    display: flex;
    justify-content: space-between;
    gap: 10px;
  }

</style>

<script lang="ts">
import { useAuth0 } from '@auth0/auth0-vue';
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import axios from 'axios'
import env_config from '../../env_config.json'


export default {
  setup () {
    const auth0 = useAuth0();
    const $q = useQuasar()
    const router = useRouter()

    const name = ref(null)
    const participants = ref(null)
    const winScore = ref(null)
    const tieScore = ref(null)
    const loseScore = ref(null)

    console.log(auth0)


    return {
      name,
      participants,
      winScore,
      tieScore,
      loseScore,
      user: auth0.user,

      async onSubmit () {
        if (!auth0.user.value) {
          $q.notify({
            message: 'Please login to create a game',
            color: 'negative',
            position: 'top'
          })
          return
        };

        try {
          const response = await axios.post(`${env_config.api}/games`, {
            name: name.value,
            participants: participants.value,
            winScore: winScore.value,
            tieScore: tieScore.value,
            loseScore: loseScore.value,
            creator: auth0.user.value.sub
          })
          console.log(response)

          router.push({
            name: 'game',
            params: { id: response.data.id }
          })

        } catch (error) {
          console.log(error)
        }
      },

      onReset () {
        name.value = null
        participants.value = null
        winScore.value = null
        tieScore.value = null
        loseScore.value = null
      }
    }
  }
}
</script>

