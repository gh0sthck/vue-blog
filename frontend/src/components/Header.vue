<script setup lang="ts">
import type { PropType } from 'vue'
interface IUser {
  id: Number,
  username: String,
  email: String,
  bio: String,
  birthday: String 
}


const header_prop = defineProps({
  user: Object as PropType<IUser> | null
})

</script>

<template>
  <header class="header">
    <div class="container">
      <nav class="navigation">
        <ul class="navigation__list">
          <li class="nav__list-item">
            <RouterLink to="/">Blogg</RouterLink>
          </li>
          <li v-if="header_prop.user" class="nav__list-item"><a href="#">Профиль</a></li>
          <li v-if="!header_prop.user" class="nav__list-item"><a href="#">Регистрация</a></li>
          <li v-if="!header_prop.user" class="nav__list-item">
            <RouterLink to="/login">Вход</RouterLink> 
          </li>
          <li v-if="header_prop.user" class="nav__list-item">
            <RouterLink to="/logout">Выход</RouterLink>
          </li>
        </ul>
      </nav>
    </div>
  </header>
</template>
