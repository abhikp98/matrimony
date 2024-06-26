"""
URL configuration for matrimony project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('logout/', views.logoutFunction, name="logout"),
    path('register/', views.registerFunction, name="register"),
    path('update-profile/', views.update_profile, name='update-profile'),
    path('profile/<username>/', views.view_profile, name='view-profile'),
    path('follow-unfollow/<username>', views.follow_unfollow, name='follow-unfollow'),
    path('requests/', views.view_requests, name="requests"),
    path('connections/', views.view_followers_list, name="connections"),
    path('accept_request/<username>', views.accept_request, name="accept_request"),
]
