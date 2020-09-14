<template>
  <div class="mt-3">
    <form @submit.prevent>
      <div class="form-row align-items-center">
        <div class="col-auto">
          <label class="sr-only" for="inlineFormInput">Search Text</label>
          <input
            type="text"
            class="form-control mb-2"
            id="inlineFormInput"
            placeholder="Search Text"
            v-model="searchText"
          />
        </div>
        <div class="col-auto">
          <button
            v-on:click="search()"
            type="submit"
            class="btn btn-primary mb-2"
          >
            Search
          </button>
        </div>
      </div>
    </form>

    <div class="card-columns">
      <div class="card" v-for="player in players" v-bind:key="player.id">
        <img
          class="card-img-top"
          v-bind:src="player.photo"
          v-bind:alt="player.name"
        />
        <div class="card-body">
          <h5 class="card-title">{{ player.name }}</h5>
          <p class="card-text"><b>Age: </b>{{ player.age }}</p>
          <p class="card-text">
            <b>Nationality: </b>{{ player.nationality.name }}
          </p>
          <p class="card-text"><b>Club: </b>{{ player.club.name }}</p>
          <p class="card-text"><b>Overall (score): </b>{{ player.overall }}</p>
          <p class="card-text">
            <b>Value: </b>€ {{ player.value.toLocaleString() }}
          </p>
        </div>
      </div>
    </div>

    <div class="d-flex justify-content-center mt-3">
      <nav aria-label="Page navigation example">
        <ul class="pagination">
          <li class="page-item">
            <a class="page-link" v-on:click="getPreviousPage()">Previous</a>
          </li>
          <li class="page-item">
            <a class="page-link">{{ response_data.page }}</a>
          </li>
          <li class="page-item">
            <a class="page-link" v-on:click="getNextPage()">Next</a>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "PlayersSearch",
  props: {
    msg: String,
  },
  data: function() {
    return {
      players: [],
      response_data: {},
      searchText: "",
    };
  },
  mounted() {
    this.getPlayers();
  },
  methods: {
    search() {
      this.getPlayers();
    },
    getPlayers(page) {
      let params = {};
      if (this.searchText) params["search"] = this.searchText;
      if (page) params["page"] = page;
      axios
        .get("http://localhost/be/players/", { params })
        .then((response) => {
          this.players = response.data.data.players;
          this.response_data = response.data.data;
        })
        .catch((e) => {
          console.log(e);
        });
    },
    getNextPage() {
      if (this.response_data.pages_count > this.response_data.page)
        this.getPlayers(this.response_data.page + 1);
    },
    getPreviousPage() {
      if (this.response_data.page > 1)
        this.getPlayers(this.response_data.page - 1);
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
