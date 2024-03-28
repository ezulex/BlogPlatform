from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post_create/', views.post_create, name='post_create'),
    path('retrieve/<int:pk>/', views.post_retrive, name='post_retrive'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.user_edit, name='user_edit'),
    path('delete/<int:pk>', views.post_delete, name='post_delete'),
    path('post_edit/<int:pk>/', views.post_edit, name='post_edit'),
    path('notifications/', views.notifications, name='notifications'),
]