<template>
  <div class="container">
    <PlayersSearch />
  </div>
</template>

<script>
// @ is an alias to /src
import PlayersSearch from "@/components/PlayersSearch.vue";

export default {
  name: "Home",
  components: {
    PlayersSearch,
  },
};
</script>
