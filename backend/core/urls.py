from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Feed
    path('', views.feed_view, name='feed'),

    # Profile
    path('profile/<str:username>/', views.profile_view, name='profile'),

    # Search
    path('search/', views.search_view, name='search'),
]