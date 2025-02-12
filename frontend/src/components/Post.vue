<script setup lang="ts">
import axios from 'axios';
import { inject, provide, reactive, ref } from 'vue'

import Comment from './Comment.vue'
import { useCookies } from 'vue3-cookies';
import type { IUser } from '@/interfaces';

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
  author: String,
  create_date: String,
  text: String
}

let text = ref<string>("");
let opened_comments = ref<Boolean>(false);
let comments = reactive<{ list: IComment[] }>({ list: [] })
let current_user: IUser | undefined | null = inject("current_user");

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
  const { cookies } = useCookies(); 
  try {
    const { data } = await axios.post("http://localhost:8000/posts/like", {
      user_id: 0,
      post_id: props_post.id,
      access_token: cookies.get("access_token")  
    }, {withCredentials: true})
  } catch (exc) {
    console.error(exc)
  }
}

const dislike = async () => {
  const { cookies } = useCookies();
  try {
    const { data } = await axios.post("http://localhost:8000/posts/dislike", {
      user_id: 0,
      post_id: props_post.id,
      access_token: cookies.get("access_token")
    }, { withCredentials: true })
  } catch (exc) {
    console.error(exc);
  }
}

const set_date = (list: IComment[]) => {
  for (let i = 0; i < list.length; i++) {
    const date = new Date(list[i].create_date);
    list[i].create_date = String(
      date.getFullYear() + "-" + date.getMonth() + "-" + date.getDate() + ", в " + date.getHours() + ":" + date.getMinutes()
    )
  }
  return list;
}

const set_comments_authors = async (list: IComment[]) => {
  for (let i = 0; i < list.length; i++) {
    try {
      const { data } = await axios.get("http://localhost:8000/users/" + String(list[i].author))
      list[i].author = data.username
    } catch (exc) {
      console.error(exc)
    }
  }
  return list 
}

const comment = async () => {
  opened_comments.value = !opened_comments.value
  if (opened_comments) {
    const { data } = await axios.get("http://localhost:8000/comments/reviews_all/" + String(props_post.id));
    comments.list = data;
    set_date(comments.list); 
    set_comments_authors(comments.list);
  }
  return comments
}

const comment_text = ref<string>("");

const set_comment = async() => {
  const { cookies } = useCookies();
  try {
    const { data } = await axios.post("http://localhost:8000/comments/" + String(props_post.id), {
      text: comment_text.value,
      author: 0, 
      access_token: cookies.get("access_token"), 
    }, {withCredentials: true});
  } catch (exc) {
    console.error(exc);
  }
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
      <a href="" @click.prevent="like()" v-if="!(props_post.is_liked) && current_user">Like</a> ({{ props_post.likes?.length }})
      <a href="" @click.prevent="dislike()" v-if="props_post.is_liked && current_user">Dislike</a>  
      <a href="" @click.prevent="comment()">Comment</a>

      <div :style="{ display: opened_comments && current_user ? 'block' : 'none' }" class="comment_form">
        <form method="post" @submit.prevent="set_comment">
          <input type="text" name="comment" v-model="comment_text">
          <input type="submit" value="Отправить">
        </form>
      </div>

      <Comment
        v-for="comment in comments.list"
        :style="{ display: opened_comments ? 'block' : 'none'}"
        :text="comment.text"
        :author="comment.author"
        :create_date="comment.create_date"
      />

    </div>
  </div>
</template>
