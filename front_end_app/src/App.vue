<template>
  <div id="app">
    <nav class="navbar navbar-dark bg-primary navbar-expand-lg">
      <a class="navbar-brand" href="#">Players App</a>
      <div class="collapse navbar-collapse" id="navbarText">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <router-link to="/" class="nav-link">Search</router-link>
          </li>
          <li class="nav-item active">
            <router-link to="/about" class="nav-link">Build A Team</router-link>
          </li>
        </ul>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<style></style>
