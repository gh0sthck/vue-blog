import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import VueCookies from 'vue3-cookies'
import App from './App.vue'

import './assets/bootstrap-reboot.min.css'
import './assets/bootstrap.min.css'
import './assets/main.css'
import Main from './components/Main.vue'
import Login from './pages/Login.vue'
import Logout from './pages/Logout.vue'
import Register from './pages/Register.vue'

const app = createApp(App)

const routes = [
  { path: "/", name: "main", component: Main },
  { path: "/login", name: "login", component: Login },
  { path: "/logout", name: "logout", component: Logout },
  { path: "/register", name: "register", component: Register },
]

export const router = createRouter({
  history: createWebHistory(),
  routes 
})

app.use(router)
app.use(VueCookies)

app.mount("#app")
