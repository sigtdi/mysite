from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.urls import reverse

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='images/avatars/%Y/%m/%d/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))])
    bio = models.TextField(max_length=500, blank=True, verbose_name='Информация о себе')

    class Meta:
        db_table = 'app_profiles'
        ordering = ('user',)
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'slug': self.slug})

    @property
    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        return f'https://ui-avatars.com/api/?size=150&background=random&name={self.slug}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    objects = models.Manager()
    contest = ''

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


