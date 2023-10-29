import { createRouter as createVueRouter, createWebHistory, type Router} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import NewGameView from '../views/NewGameView.vue'
import GameView from '../views/GameView.vue'
import { createAuthGuard } from "@auth0/auth0-vue";
import type { App } from 'vue';


export default function createRouter(app: App): Router {
  return createVueRouter({
    routes: [
      {
        path: "/",
        name: "home",
        component: HomeView
      },
      {
        path: "/new-game",
        name: "create-game",
        component: NewGameView,
        beforeEnter: createAuthGuard(app)
      },
      {
        path: "/game/:id",
        name: "game",
        component: GameView,
      },
      {
        path: "/:pathMatch(.*)*",
        redirect: "/"
      }
    ],

    history: createWebHistory()
  })
}
