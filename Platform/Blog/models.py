from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Текст поста")
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_posted']  # sort from new to old

    def save(self, *args, **kwargs):
        if not self.pk:  # only create
            self.author = self.request.user
        super().save(*args, **kwargs)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(verbose_name="")
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # only create
            self.author = self.request.user
        super().save(*args, **kwargs)