from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Contest, Profile
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

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


def profile(request):
    posts_temp = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = []
    for post in posts_temp:
        if post.author == request.user:
            posts.append(post)

    return render(request, "blog/profile.html", {'posts': posts})


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'base/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context