from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    objects = models.Manager()
    contest = ''
    likes = 0

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def more_likes(self):
        self.likes += 1

    def __str__(self):
        return self.title


class Contest(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True)
    objects = models.Manager()
    posts = []
    likes = 0

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def more_likes(self):
        self.likes += 1

    def add_post(self):
        self.posts.append(Post())

    def __str__(self):
        return self.title


class Comments(models.Model):
    pass


