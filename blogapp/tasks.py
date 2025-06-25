from .models import Post, Comment
from celery import shared_task



@shared_task
def send_comment_update(post_id, comment_id, reply_text=None):
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=comment_id)
    if reply_text:
        pass
    else:
       pass