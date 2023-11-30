from django.conf import settings
from django.db import models
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.models import User


class Profile(DetailView):
    template_name = 'blog/profile.html'
    queryset = User.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("username")
        user = get_object_or_404(User, username=id_)
        return user

    def get_context_data(self, *args, **kwargs):
        context = super(Profile, self).get_context_data(*args, **kwargs)
        user = self.get_object()
        context.update({'posts': user.posts.all().filter(created_date__lte=timezone.now()).order_by(' -created_date')})


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='static/images')
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    objects = models.Manager()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

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


