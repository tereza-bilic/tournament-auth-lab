<template>
  <div class="q-pa-md" style="max-width: 350px">
    <q-list bordered separator>
      <q-item-label header>Leaderboard</q-item-label>
      <template v-for="p in participantScoreMap">
        <q-item>
          <q-item-section>{{p.participant }}</q-item-section>
          <q-item-section side top>{{p.score}}</q-item-section>
        </q-item>
      </template>
    </q-list>
  </div>
</template>

<script setup lang="ts">
  import { ref, watch } from 'vue'
  const props = defineProps(['matches', 'participants', 'win', 'lose', 'tie'])

  watch(props.matches, () => {
    participantScoreMap.value = props.participants?.map((participant: string) => {
      const wonMatches = props.matches.filter((match: any) => match.score === participant)
      const tiedMatches = props.matches.filter((match: any) => match.score === 'Tie')
      const lostMatches = props.matches.filter((match: any) => match.score !== participant && match.score !== 'Tie' && match.score !== 0)

      const score = wonMatches.length * props.win + lostMatches.length * props.lose + tiedMatches.length * props.tie
      return {
        participant: participant,
        score
      }
    })
    .sort((a: any, b: any) => b.score - a.score)
  })

  let participantScoreMap = ref(props.participants?.map((participant: string) => {
    const wonMatches = props.matches.filter((match: any) => match.score === participant)
    const tiedMatches = props.matches.filter((match: any) => match.score === 'Tie')
    const lostMatches = props.matches.filter((match: any) => match.score !== participant && match.score !== 'Tie' && match.score !== 0)

    const score = wonMatches.length * props.win + lostMatches.length * props.lose + tiedMatches.length * props.tie
    return {
      participant: participant,
      score
    }
  })
  .sort((a: any, b: any) => b.score - a.score))

</script>
