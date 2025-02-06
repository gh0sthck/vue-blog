<script setup lang="ts">
import { reactive, ref, watch, onMounted } from 'vue'
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

const sort_by = ref<string>("");

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

//async function get_posts(sort: string | null) {
//  try {
//    if (sort == null) {
//      const { data } = await axios.get("http://localhost:8000/posts/all")
//    } else {
//      const { data } = await axios.get("http://localhost:8000/posts/all?sort_by=" + sort)
//    }
//    console.log(data)
//    return data
//  } catch (exc) {
//
//    console.error(exc);
//    return null;
//  }
//}

async function set_authors(posts_list: IPost[]) {
  for (let i = 0; i < posts_list.length; i++) {
    const auth_id = posts_list[i].author;
    const { data } = await axios.get("http://localhost:8000/users/" + String(auth_id));
    posts_list[i].author = data.username;
    const date = new Date(posts.list[i].created_date)
    posts_list[i].created_date = String(date.getFullYear() + "-" + date.getMonth() + "-" + date.getDate());
  }
  return posts
}

onMounted(async () => {
  posts.list = await get_posts(null);
  await set_authors(posts.list);
})


watch(sort_by, async () => {
  posts.list = await get_posts(sort_by.value)
  await set_authors(posts.list)
})

</script>

<template>
  <main class="main">
    <div class="container">
      <select @change="on_sort_change" name="sort" id="sort">
        <option value="all">Все</option>
        <option value="newest">Новые</option>
        <option value="oldest">Старые</option>
        <option value="today">За сегодня</option>
        <option value="title">По название</option>
      </select>
      <div class="posts">
        <Post v-for="post in posts.list" v-key="post.id" :title="post.title" :author="post.author"
          :created_date="post.created_date" />
      </div>
    </div>
  </main>
</template>
