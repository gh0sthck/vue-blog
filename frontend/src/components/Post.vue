<script setup lang="ts">
const props_post = defineProps({
  id: Number, 
  title: String,
  text: String,
  author: String,
  created_date: String, 
})
</script>

<template>
  <a href="#" class="post">
    <div class="post__wrapper">
      <h1 class="post_title">{{ props_post.title }}</h1>
      <p class="post_desc">от {{ props_post.author }}, {{ props_post.created_date }}</p>
    </div>
  </a>
</template>
