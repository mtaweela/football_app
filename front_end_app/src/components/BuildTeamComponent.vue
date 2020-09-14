<template>
  <div class="mt-3">
    <form @submit.prevent>
      <h4>Enter value in Euro to get a team</h4>
      <div class="form-row align-items-center">
        <div class="col-auto">
          <label class="sr-only" for="inlineFormInput">Build Team</label>
          <input
            type="number"
            class="form-control mb-2"
            id="inlineFormInput"
            placeholder="Add value in Euro"
            v-model="priceValue"
          />
        </div>
        <div class="col-auto">
          <button v-on:click="search()" type="submit" class="btn btn-primary mb-2">Build Team</button>
        </div>
      </div>
    </form>

    <div v-if="loading" class="mt-3">
      <h4>Loading .....</h4>
    </div>
    <div v-if="!loading" class="mt-3">
      <hr />
      <h4>Total to pay:</h4>
      <p>{{ response_data.total.toLocaleString() }}</p>
      <h4>Team:</h4>
      <div class="card-columns">
        <div class="card" v-for="player in players" v-bind:key="player.id">
          <img class="card-img-top" v-bind:src="player.photo" v-bind:alt="player.name" />
          <div class="card-body">
            <h5 class="card-title">{{ player.name }}</h5>
            <p class="card-text">
              <b>Age:</b>
              {{ player.age }}
            </p>
            <p class="card-text">
              <b>Nationality:</b>
              {{ player.nationality.name }}
            </p>
            <p class="card-text">
              <b>Club:</b>
              {{ player.club.name }}
            </p>
            <p class="card-text">
              <b>Overall (score):</b>
              {{ player.overall }}
            </p>
            <p class="card-text">
              <b>Value:</b>
              € {{ player.value.toLocaleString() }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "BuildTeamComponent",
  props: {
    msg: String,
  },
  data: function () {
    return {
      players: [],
      response_data: {},
      priceValue: undefined,
      loading: false,
    };
  },
  methods: {
    search() {
      this.getTeam();
    },
    getTeam() {
      this.players = [];
      this.response_data = {};

      let params = {};
      if (!this.priceValue) return;

      this.loading = true;
      params["total"] = this.priceValue;
      axios
        .get("https://football.dev01.dev/be/best_team/", { params })
        .then((response) => {
          this.players = response.data.data.players;
          this.response_data = response.data.data;
          this.loading = false;
        })
        .catch((e) => {
          console.log(e);
          this.loading = false;
        });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
