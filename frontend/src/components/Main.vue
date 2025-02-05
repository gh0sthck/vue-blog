<script setup lang="ts">
import { reactive, onMounted } from 'vue'
import axios from 'axios'

import Post from './Post.vue'

interface IPost {
  id: number,
  title: string,
  author: string,
  text: string,
  created_date: string
};

let posts = reactive<{ list: IPost[] }>({
  list: []
});

onMounted(async () => {
  try {
    const { data } = await axios.get("http://localhost:8000/posts/all/");
    posts.list = data;
    for (let i = 0; i < posts.list.length; i++) {
      const auth_id = posts.list[i].author;
      const { data } = await axios.get("http://localhost:8000/users/" + String(auth_id));
      posts.list[i].author = data.username;
      const date = new Date(posts.list[i].created_date)
      console.log(date);
      posts.list[i].created_date = String(date.getFullYear() + "-" + date.getMonth() + "-" + date.getDate());
    
    }
  } catch (ex) {
    console.error(ex)
  }
})


</script>

<template>
  <main class="main">
    <div class="container">
      <div class="posts">
        <Post v-for="post in posts.list" v-key="post.id" :title="post.title" :author="post.author"
          :created_date="post.created_date" />
      </div>
    </div>
  </main>
</template>
