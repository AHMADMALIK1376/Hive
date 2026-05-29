from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """A post created by a user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=500)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Newest posts first

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}..."

    def likes_count(self):
        return self.likes.count()

    def comments_count(self):
        return self.comments.count()

class Comment(models.Model):
    """A comment on a post"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']  # Oldest comments first

    def __str__(self):
        return f"{self.user.username}: {self.body[:30]}..."