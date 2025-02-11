<script setup lang="ts">
import axios from 'axios';
import { router } from '../main'
import { useCookies } from 'vue3-cookies';

const { cookies } = useCookies();

const logout = async () => {
  try {
    const { data } = await axios.post("http://localhost:8000/users/logout", {
      access_token: cookies.get("access_token"),
    }, { withCredentials: true })
    router.push("/login")
  } catch (exc) {
    console.error(exc)
  }
}
</script>
<template>
  <div class="container">
    <form @submit.prevent="logout">
      <p>Вы действительно хотите выйти из аккаунта?</p>
      <input type="submit" value="Выйти">
    </form>
  </div>
</template>
