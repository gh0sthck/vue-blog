import datetime
from pydantic import BaseModel


class SReview(BaseModel):
    text: str
    author: int


class SReviewView(SReview):
    id: int
    create_date: datetime.datetime


class SComment(BaseModel):
    post_id: int
    review_id: int


class SCommentView(SComment):
    id: int
