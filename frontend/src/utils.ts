import axios from 'axios'
import type { IPost, IUser } from './interfaces'

export async function set_authors(posts_list: IPost[]) {
  for (let i = 0; i < posts_list.length; i++) {
    const auth_id = posts_list[i].author
    const { data } = await axios.get('http://localhost:8000/users/' + String(auth_id))
    posts_list[i].author = data.username
    const date = new Date(posts_list[i].created_date)
    posts_list[i].created_date = String(
      date.getFullYear() + '-' + date.getMonth() + '-' + date.getDate(),
    )
  }
  return posts_list
}

export async function set_likes(
  posts_list: IPost[],
  current_user: IUser | null | undefined = null,
) {
  for (let i = 0; i < posts_list.length; i++) {
    const pid = posts_list[i].id
    const { data } = await axios.get('http://localhost:8000/posts/likes/' + String(pid))
    posts_list[i].likes = data
    if (current_user.value) {
      if (data.includes(current_user.value.id)) {
        posts_list[i].is_liked = true
      } else {
        posts_list[i].is_liked = false
      }
    } else {
      posts_list[i].is_liked = false
    }
  }
  return posts_list
}

export async function get_comments(post_list: IPost[]) {
  for (let i = 0; i < post_list.length; i++) {
    const { data } = await axios.get(
      'http://localhost:8000/comments/reviews_all/' + String(post_list[i].id),
    )
    post_list[i].comments_count = data.length
  }
  return post_list
}
