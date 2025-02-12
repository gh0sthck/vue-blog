<script setup lang="ts">
import type { PropType } from 'vue'
import type { IUser } from '@/interfaces'

const header_prop = defineProps({
  user: Object as PropType<IUser | undefined | null>
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
          <li v-if="header_prop.user" class="nav__list-item">
            <RouterLink to="/profile">{{ header_prop.user.username }}</RouterLink>
          </li>
          <li v-if="!header_prop.user" class="nav__list-item">
            <RouterLink to="/register">Регистрация</RouterLink>
          </li>
          <li v-if="!header_prop.user" class="nav__list-item">
            <RouterLink to="/login">Вход</RouterLink> 
          </li>
          <li v-if="header_prop.user" class="nav__list-item">
            <RouterLink class="btn btn-danger" to="/logout">Выход</RouterLink>
          </li>
        </ul>
      </nav>
    </div>
  </header>
</template>
