<script setup lang="ts">
import { ref } from 'vue'

const props_post = defineProps({
  id: Number,
  title: String,
  text: String,
  author: String,
  created_date: String,
})

let text = ref<string>("");

for (let i = 0; i < props_post.text?.length / 2; i++) {
  text.value += props_post.text[i];
}

function set_full_text() {
  text.value = props_post.text;
  return props_post.text;
}

function like() {
  console.log("liking...")
}

function comment() {
  console.log("commenting...")
}
</script>

<template>
  <div href="#" class="post">
    <div class="post__wrapper">
      <h1 class="post_title">{{ props_post.title }}</h1>
      <p class="post_desc">от {{ props_post.author }}, {{ props_post.created_date }}</p>
      <a draggable="false" class="post_content" href="#">
        <p class="post_text">
          {{ text }}
          <a @click="set_full_text" v-if="text.length != props_post.text?.length">Далее...</a>
        </p>
      </a>
      <a href="">Like</a>
      <a href="">Comment</a>
    </div>
  </div>
</template>
