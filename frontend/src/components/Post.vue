<script setup lang="ts">
import axios from 'axios';
import { onMounted, reactive, ref } from 'vue'

const props_post = defineProps({
  id: Number,
  title: String,
  text: String,
  author: String,
  created_date: String,
  likes: Array,
  is_liked: Boolean
})

let text = ref<string>("");

for (let i = 0; i < props_post.text?.length / 2; i++) {
  text.value += props_post.text[i];
}

function set_full_text() {
  text.value = props_post.text;
  return props_post.text;
}

const like = async () => {
  try {
    console.log("props likes", props_post.likes)
    const { data } = await axios.post("http://localhost:8000/posts/like", {
      user_id: 31,
      post_id: props_post.id
    })
    console.log(data);
  } catch (exc) {
    console.error(exc)
  }
}

const dislike = async () => {
  try {
    const { data } = await axios.post("http://localhost:8000/posts/dislike", {
      user_id: 31,
      post_id: props_post.id
    })
    console.log(data);
  } catch (exc) {
    console.error(exc);
  }
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
          <a href="" @click.prevent="set_full_text" v-if="text.length != props_post.text?.length">Далее...</a>
        </p>
      </a>
      <a href="" @click.prevent="like()" v-if="!props_post.is_liked">Like ({{ props_post.likes?.length }})</a>
      <a href="" @click.prevent="dislike()" v-if="props_post.is_liked">Dislike ({{ props_post.likes?.length }})</a>
      <a href="" @click.prevent="comment()">Comment</a>
    </div>
  </div>
</template>
