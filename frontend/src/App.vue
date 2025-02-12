<script setup lang="ts">
import { onMounted, provide, ref } from 'vue';
import axios from 'axios'
import { useCookies } from 'vue3-cookies';

import Header from './components/Header.vue'
import type { IUser } from './interfaces';

let current_user = ref<IUser | undefined | null>(null);

const get_current_user = async () => {
  const { cookies } = useCookies();
  let user: IUser; 
  try {
    const { data } = await axios.get("http://localhost:8000/users/me", {
      headers: {
        Authorization: `Bearer ${cookies.get("access_token")}`,
        Cookie: `access_token=${cookies.get("access_token")}`
      },
      withCredentials: true
    },)
    user = data;
    return user;
  } catch (exc) {
  }
}

provide("current_user", current_user);

onMounted(async () => {
  current_user.value = await get_current_user();
})
</script>


<template>
  <Header :user="current_user" />

  <router-view></router-view>
</template>
