from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    bio = models.TextField()
    is_verified = models.BooleanField(default=False)


    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    category = models.CharField(max_length=100)
    published_date = models.DateField()
    likes = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)


    @property
    def level(self):
        level = 0
        parent = self.parent
        while parent is not None:
            level += 1
            parent = parent.parent
        return level

    def __str__(self):
        return f'комментарий {self.author} для {self.post}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"Изображение для поста {self.post.id}"
