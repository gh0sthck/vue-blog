import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

import './assets/bootstrap-reboot.min.css'
import './assets/bootstrap.min.css'
import './assets/main.css'
import Main from './components/Main.vue'
import Login from './pages/Login.vue'

const app = createApp(App)

const routes = [
  { path: "/", name: "main", component: Main },
  { path: "/login", name: "login", component: Login }
]

const router = createRouter({
  history: createWebHistory(),
  routes 
})

app.use(router)

app.mount("#app")
