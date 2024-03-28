from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    post_id = models.TextField(null=True)
    post_name = models.TextField(null=True)


@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, created, **kwargs):
    if created:
        post_author = instance.post.author
        comment_author = instance.author
        post_title = instance.post.title
        date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        id = instance.post.id

        Notification.objects.create(
            user=post_author,
            message=f"{date}: Пользователь {comment_author.username} оставил новый комментарий к вашему посту ",
            post_name=post_title,
            post_id=id
        )