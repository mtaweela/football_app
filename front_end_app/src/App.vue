<template>
  <div id="app">
    <nav class="navbar navbar-dark bg-primary navbar-expand-lg">
      <a class="navbar-brand" href="#">Players App</a>
      <div class="collapse navbar-collapse" id="navbarText">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <a class="nav-link" href="#">Search</a>
          </li>
          <li class="nav-item active">
            <a class="nav-link" href="#">Compose a Team</a>
          </li>
        </ul>
      </div>
    </nav>
    <div class="container">
      <PlayersSearch msg="Welcome to Your Vue.js App" />
    </div>
  </div>
</template>

<script>
import PlayersSearch from "./components/PlayersSearch.vue";

export default {
  name: "App",
  components: {
    PlayersSearch,
  },
};
</script>

<style></style>
