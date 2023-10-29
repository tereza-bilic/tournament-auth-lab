<template>
  <div class="q-pa-md" style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px">
    <template v-for="(match, index) in matches">
      <match :match="match" :round="index + 1" :isEditable="props.isEditable" :updateMatch="updateMatch"/>
    </template>
  </div>
</template>

<script setup lang="ts">
  import Match from '@/components/Match.vue'
  const props = defineProps(['matches', 'isEditable', 'updateMatch'])

</script>
