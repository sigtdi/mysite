from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    #path('', views.contest_list, name='contests_list'),
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path('post/new/', views.post_new, name='post_new'),
    path("accounts/profile/", views.profile, name="profile"),
    path('profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='profile'),
]