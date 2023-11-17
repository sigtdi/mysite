from django.contrib import admin
from .models import Post, Profile

admin.site.register(Post)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug')
    list_display_links = ('user', 'slug')