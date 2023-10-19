from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Contest
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def contest_list(request):
    contests = Contest.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/contests_list.html', {'contests': contests})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def home_page(request):
    return render(request, 'blog/home_page.html')


def home(request):
    return render(request, "users/home.html")


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
