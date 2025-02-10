<script setup lang="ts">
import axios from 'axios';
import { reactive, ref } from 'vue'

import Comment from './Comment.vue'

const props_post = defineProps({
  id: Number,
  title: String,
  text: String,
  author: String,
  created_date: String,
  likes: Array,
  is_liked: Boolean
})

interface IComment {
  id: Number,
  author: Number,
  create_date: String,
  text: String
}

let text = ref<string>("");
let opened_comments = ref<Boolean>(false);
let comments = reactive<{ list: IComment[] }>({ list: [] })

function close_text() {
    text.value = "";
    for (let i = 0; i < props_post.text?.length / 2; i++) {
      text.value += props_post.text[i];
    }
}

close_text();

function set_full_text() {
  if (text.value.length != props_post.text?.length) {
    text.value = props_post.text;
    return props_post.text;
  } else { 
    close_text()
  }
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

const set_date = (list: IComment[]) => {
  for (let i = 0; i < list.length; i++) {
    const date = new Date(list[i].create_date);
    list[i].create_date = String(
      date.getFullYear() + "-" + date.getMonth() + "-" + date.getDate() + ", в " + date.getHours() + ":" + date.getMinutes() )
  }
  return list;
}

const comment = async () => {
  opened_comments.value = !opened_comments.value
  console.log(1234, opened_comments.value)
  if (opened_comments) {
    const { data } = await axios.get("http://localhost:8000/comments/reviews_all/" + String(props_post.id));
    comments.list = data;
    comments.list = set_date(comments.list); 
    console.log("comments", comments.list)
  }
  return comments
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
          <a 
            href=""
            @click.prevent="set_full_text"
            :style="{ display: text.length != props_post.text?.length ? 'inline' : 'none'}"
          >
            Далее...
          </a>
          <a 
            href=""
            @click.prevent="set_full_text" 
            :style="{ display: text.length == props_post.text?.length ? 'inline' : 'none'}"
          >
            Свернуть
          </a>
        </p>
      </a>
      <a href="" @click.prevent="like()" v-if="!props_post.is_liked">Like ({{ props_post.likes?.length }})</a>
      <a href="" @click.prevent="dislike()" v-if="props_post.is_liked">Dislike ({{ props_post.likes?.length }})</a>
      <a href="" @click.prevent="comment()">Comment</a>

      <Comment
        v-for="comment in comments.list"
        :style="{ display: opened_comments ? 'block' : 'none'}"
        :text="comment.text"
        :author="props_post.author"
        :create_date="comment.create_date"
      />
    </div>
  </div>
</template>
