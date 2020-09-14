import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/build-team',
    name: 'BuildTeam',
    component: () => import('../views/BuildTeam.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
