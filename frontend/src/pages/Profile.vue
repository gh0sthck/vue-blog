<script setup lang="ts">
import { inject, onMounted, reactive, ref } from 'vue';
import { useCookies } from 'vue3-cookies';
import axios from 'axios';

import Post from '../components/Post.vue';
import { type IPost, type IUser } from '@/interfaces';
import { set_authors } from '@/utils';
import { set_likes } from '@/utils';

let user_posts = reactive<{ ls: IPost[] }>({
  ls: []
})
let current_user: IUser | null | undefined = inject<IUser | null | undefined>("current_user");
let post_title = ref<string>("");
let post_text = ref<string>("");

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

const get_posts = async () => {
  try {
    const { data } = await axios.get("http://localhost:8000/posts/by_user/" + String(current_user.value.id));
    return data
  } catch (exc) {
    console.error(exc)
  }
}

const set_post = async () => {
  const { cookies } = useCookies();
  try {
    const { data } = await axios.post("http://localhost:8000/posts/add", {
      title: post_title.value,
      text: post_text.value,
      author: 0,
      access_token: cookies.get("access_token"),
    }, { withCredentials: true })
  } catch (exc) {
    console.error(exc);
  }
}


onMounted(async () => {
  current_user.value = await get_current_user();
  user_posts.ls = await get_posts();
  user_posts.ls = await set_authors(user_posts.ls);
  user_posts.ls = await set_likes(user_posts.ls, current_user);
})
</script>

<template>
  <div class="container">
    <h1 class="profile__title">
      {{ current_user?.username }}
    </h1>
    <div v-if="current_user" class="profile__posts">
      <h3>Создать запись</h3>
      <form @submit.prevent="set_post" class="profile__posts-form">
        <input type="text" v-model="post_title" name="title" />
        <textarea name="text" v-model="post_text"></textarea>
        <input type="submit" value="Отправить">
      </form>
      <div class="posts">
        <Post v-for="post in user_posts.ls" v-bind:key="post.id" :id="post.id" :title="post.title" :text="post.text"
          :created_date="post.created_date" :author="current_user?.username" :likes="post.likes"
          :is_liked="post.is_liked" />
      </div>
    </div>
  </div>
</template>
