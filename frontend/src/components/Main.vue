<script setup lang="ts">
import { reactive, ref, watch, onMounted, inject } from 'vue'
import axios from 'axios'

import Post from './Post.vue'
import type { IPost, IUser } from '@/interfaces';
import { set_authors, set_likes } from '@/utils';


let posts = reactive<{ list: IPost[] }>({
  list: []
});
let sort_by = ref<string>("");
let current_user: IUser | null | undefined = inject("current_user")

function on_sort_change(event: any) {
  sort_by.value = event.target.value
}

async function get_posts(sort: string | null) {
  if (sort == null) {
    try {
      const { data } = await axios.get("http://localhost:8000/posts/all")
      return data;
    }
    catch (exc) {
      console.error(exc)
      return null
    }
  } else {
    try {
      const { data } = await axios.get("http://localhost:8000/posts/all?sort_by=" + sort)
      return data;
    } catch (exc) {
      console.error(exc);
      return null;
    }
  }
}


onMounted(async () => {
  posts.list = await get_posts(null);
  posts.list = await set_authors(posts.list);
  posts.list = await set_likes(posts.list, current_user);
})


watch(sort_by, async () => {
  posts.list = await get_posts(sort_by.value)
  await set_authors(posts.list)
  await set_likes(posts.list)
})

</script>

<template>
  <main class="main">
    <div class="container">
      <div class="posts">
        <select @change="on_sort_change" name="sort" id="sort">
          <option value="all">Все</option>
          <option value="newest">Новые</option>
          <option value="oldest">Старые</option>
          <option value="today">За сегодня</option>
          <option value="title">По название</option>
        </select>
        <Post v-for="post in posts.list" v-key="post.id" :id="post.id" :title="post.title" :author="post.author"
          :created_date="post.created_date" :text="post.text" :likes="post.likes" :is_liked="post.is_liked" />
      </div>
    </div>
  </main>
</template>
