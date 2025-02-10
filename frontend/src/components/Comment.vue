<script setup lang="ts">
import { defineProps } from 'vue';

const comment_prop = defineProps({
  author: String,
  create_date: String,
  text: String
})
</script>

<template>
  <div class="comment">
    <h4 class="comment__author"> {{ comment_prop.author }}, <span class="comment__date">{{ comment_prop.create_date }}
      </span></h4>
    <p class="comment__text">{{ comment_prop.text }}</p>
  </div>
</template>
