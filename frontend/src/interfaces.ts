export interface IUser {
  id: Number,
  username: String,
  email: String,
  bio: String,
  birthday: String
}

export interface IPost {
  id: number,
  title: string,
  author: string,
  text: string,
  created_date: string,
  likes: number[],
  is_liked: boolean,
  comments_count: number,
};
