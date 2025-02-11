<script setup lang="ts">
import axios from 'axios';
import { ref } from 'vue';
import { router } from '@/main';

const username = ref<string>("");
const password = ref<string>("");
const email = ref<string>("");
const bio = ref<string>("");
const birthday = ref<string>("");

const register = async () => {
  try {
    const { data } = await axios.post("http://localhost:8000/users/register", {
      username: username.value,
      password: password.value,
      email: email.value,
      bio: bio.value,
      birthday: birthday.value, 
    })
 
    router.push("/login");
  } catch (exc) {
    console.error(exc)
  }
}

</script>

<template>
  <div class="container">
    <h2>Регистрация</h2>
    <form method="post" @submit.prevent="register">
      <input type="text" placeholder="Имя пользователя" name="username" v-model="username" />
      <input type="password" placeholder="Пароль" name="password" v-model="password" />
      <input type="email" placeholder="Электронная почта" name="email" v-model="email" />
      <textarea name="bio" placeholder="О себе" v-model="bio" cols="40" rows="5"></textarea>
      <input type="date" name="birthday" v-model="birthday" />
      <input type="submit" value="Зарегестрироваться"> 
    </form>
  </div>
</template>

<style scoped>
input, textarea {
  border: 2px solid black;
  border-radius: 30px;
}
</style>
