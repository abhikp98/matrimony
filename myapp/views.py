from django.http import HttpResponse
from django.shortcuts import render, redirect

from myapp.models import Followers, UserProfile
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages


# Create your views here.

def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            messages.warning(request, "Password is Incorrect, Try again")
        else:
            messages.warning(request, "No account in this Username")


    elif request.user.is_authenticated:
        return redirect('home')
    context = {'form': LoginForm}
    return render(request, 'login.html', context)


def registerFunction(request):
    form = RegisterForm()
    context = {'form': form}
    return render(request, 'register.html', context)



def logoutFunction(request):
    logout(request)
    return redirect('index')


def home(request):
    users = UserProfile.objects.all().exclude(user=request.user)
    isProfile = False
    if UserProfile.objects.filter(user=request.user).exists():
        isProfile = True
    context = {"users": users, "isProfile": isProfile}
    return render(request, 'home.html', context)


def view_requests(request):
    followers = Followers.objects.filter(profile=request.user, approved=False)
    context = {"followers": followers}
    return render(request, 'followers.html', context)


def view_followers_list(request):
    followers = Followers.objects.filter(profile=request.user, approved=False)
    context = {"followers": followers}
    return render(request, 'followers_list.html', context)


def follow_unfollow(request, ):
    return None


def update_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            frm = form.save(commit=False)
            frm.user = request.user
            frm.save()
            return redirect('')
    if UserProfile.objects.filter(user=request.user).exists():
        userprofile = UserProfile.objects.get(user=request.user)
        form = UserProfile(instance=userprofile)
    context = {"form": form}
    return render(request, 'update-profile.html', context)


def view_profile(request, username):
    if not UserProfile.objects.filter(user=request.user).exists():
        return redirect('update-profile')
    obj = UserProfile.objects.get(user__username=username)
    context = {"profile": obj}
    return render(request, 'view-profile.html', context)

