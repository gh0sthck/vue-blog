<script setup lang="ts">
import axios from 'axios';
import { ref } from 'vue'
import { router } from '../main'
import { useCookies } from 'vue3-cookies';

let username = ref<string>("")
let password = ref<string>("")


const login = async () => {
  const params = new URLSearchParams();
  params.append("username", username.value);
  params.append("password", password.value);
  const { cookies } = useCookies();
  try {
    const response = await axios.post("http://localhost:8000/users/login", params)
    cookies.set("access_token", response.data.token);
    router.push("/") 
  } catch (exc) {
    console.error(exc)
  } 
}

</script>

<template>
  <div class="container">
    <h1>Вход</h1>
    <form style="display: flex; flex-direction: column;" method="post" @submit.prevent="login">
      <input type="text" placeholder="Имя пользователя" v-model="username" name="username">
      <input type="password" placeholder="Пароль" v-model="password" name="password" id="">
      <input type="submit" value="Войти">
    </form>
  </div>
</template>
