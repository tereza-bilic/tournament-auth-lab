<template>
  <q-card dark bordered class="bg-grey-3 my-card text-dark" >
    <q-card-section style="display: flex; justify-content: space-between;">
      <span> Round {{round}} </span>
      <span class="text-right">Result</span>
    </q-card-section>

    <q-separator inset/>

    <q-card-section  style="display: flex; width: 20rem; justify-content: space-between; align-items: center;">
      {{match.player1}} <span class="text-primary" style="padding: 4px">vs</span> {{match.player2}}
      <template v-if="props.isEditable">
        <q-select style="width: 10rem" square outlined v-model="score" :options="options"/>
      </template>
      <template v-else>
        <span>{{score}}</span>
      </template>
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">
import { reactive, ref, watch } from 'vue'
const props = defineProps(['match', 'round', 'isEditable', 'updateMatch'])
const match = reactive(props.match)
const score = ref(props.match.score)
const options = [match.player1, match.player2, 'Tie']

watch(score, async (newVal) => {
  await props.updateMatch(match, newVal)
})
</script>
