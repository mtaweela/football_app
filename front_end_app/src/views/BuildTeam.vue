<template>
  <div class="container">
    <BuildTeamComponent />
  </div>
</template>

<script>
// @ is an alias to /src
import BuildTeamComponent from "@/components/BuildTeamComponent.vue";

export default {
  name: "BuildTeam",
  components: {
    BuildTeamComponent,
  },
};
</script>
