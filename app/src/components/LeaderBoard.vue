<template>
  <div class="q-pa-md bg-grey-9 text-white" style="min-width: 350px">
    <q-list dark bordered separator>
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
  import { computed, ref, watch } from 'vue'
  const props = defineProps(['matches', 'participants', 'win', 'lose', 'tie'])

  const participantScoreMap = computed(() => props.participants?.map((participant: string) => {
    const participantMatches = props.matches.filter((match: any) => match.player1 === participant || match.player2 === participant)
    const wonMatches = participantMatches.filter((match: any) => match.score === participant)
    const tiedMatches = participantMatches.filter((match: any) => match.score === 'Tie')
    const lostMatches = participantMatches.filter((match: any) => match.score !== participant && match.score !== 'Tie' && match.score !== 0)

    const score = wonMatches.length * props.win + lostMatches.length * props.lose + tiedMatches.length * props.tie
    return {
      participant: participant,
      score
    }
  })
  .sort((a: any, b: any) => b.score - a.score))
</script>
