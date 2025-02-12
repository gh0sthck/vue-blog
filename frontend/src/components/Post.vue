<script setup lang="ts">
import axios from 'axios';
import { inject, reactive, ref } from 'vue'

import Comment from './Comment.vue'
import { useCookies } from 'vue3-cookies';
import type { IUser } from '@/interfaces';
import { router } from '@/main';

const props_post = defineProps({
  id: Number,
  title: String,
  text: String,
  author: String,
  created_date: String,
  likes: Array,
  is_liked: Boolean,
  comments_count: Number,
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
    }, { withCredentials: true })
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

const set_comment = async () => {
  const { cookies } = useCookies();
  try {
    const { data } = await axios.post("http://localhost:8000/comments/" + String(props_post.id), {
      text: comment_text.value,
      author: 0,
      access_token: cookies.get("access_token"),
    }, { withCredentials: true });
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
      <p draggable="false" class="post_content">
        <p class="post_text">
          {{ text }}
          <a href="" @click.prevent="set_full_text"
            :style="{ display: text.length != props_post.text?.length ? 'inline' : 'none' }">
            Далее...
          </a>
          <a href="" @click.prevent="set_full_text"
            :style="{ display: text.length == props_post.text?.length ? 'inline' : 'none' }">
            Свернуть
          </a>
        </p>
      </p>
      <div class="post__interact">
        <span style="margin-right: 8px; font-size: 20px;">
          {{ props_post.likes?.length }}
        </span>
        <a href="" @click.prevent="like()" v-if="!(props_post.is_liked) && current_user">
          <img style="height: 25px; width: 25px;" src="../assets/images/notlike.png" alt="Like">
        </a>
        <a href="" @click.prevent="dislike()" v-if="props_post.is_liked && current_user">
          <img style="height: 25px; width: 25px;" src="../assets/images/like.png" alt="Like">
        </a>
        <a href="" @click.prevent="router.push('/login')" v-if="!current_user">
          <img style="height: 25px; width: 25px;" src="../assets/images/notlike.png" alt="not register" />
        </a>
        <span style="margin-left: 8px;">
          {{ props_post.comments_count }}
        </span>
        <a href="" @click.prevent="comment()">
          <img style="height: 28px; width: 25px; margin-left: 5px;" src="../assets/images/comment.png" alt="comment">
        </a>
      </div>

      <div :style="{ display: opened_comments && current_user ? 'block' : 'none' }" class="comment_form">
        <form method="post" @submit.prevent="set_comment">
          <input type="text" placeholder="Комментарий..." name="comment" v-model="comment_text">
          <input type="submit" value="Отправить">
        </form>
        <p v-if="comments.list.length == 0">
          Оставьте первый комментарий!
        </p>
      </div>

      <Comment v-for="comment in comments.list" :style="{ display: opened_comments ? 'block' : 'none' }"
        :text="comment.text" :author="comment.author" :create_date="comment.create_date" />
    </div>
  </div>
</template>
