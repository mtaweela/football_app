<template>
  <div id="app">
    <nav class="navbar navbar-dark bg-primary navbar-expand-lg">
      <router-link to="/" class="navbar-brand"
        >Foot Ball Players App</router-link
      >

      <div class="collapse navbar-collapse" id="navbarText">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <router-link to="/" class="nav-link">Search</router-link>
          </li>
          <li class="nav-item active">
            <router-link to="/build-team" class="nav-link"
              >Build A Team</router-link
            >
          </li>
        </ul>
      </div>
    </nav>
    <router-view />
  </div>
</template>
