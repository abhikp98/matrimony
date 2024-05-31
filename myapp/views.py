import profile
from django.http import HttpResponse
from django.shortcuts import render, redirect

from myapp.models import Followers, Photos, UserProfile
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required

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
    return render(request, 'index.html', context)


def registerFunction(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            usr = authenticate(request, username=username, password=password)
            if usr is not None:
                login(request, usr)
                return redirect('home')
            else:
                messages.error(request, "Authentication failed Login again")
        else:
            messages.error(request, "invalid form submission")
    form = RegisterForm()
    context = {'form': form}
    return render(request, 'register.html', context)



def logoutFunction(request):
    logout(request)
    return redirect('index')

@login_required(login_url="/")
def home(request):
    userlist = []
    for i in Followers.objects.filter(profile__user=request.user):
        userlist.append(i.sender)
    users = UserProfile.objects.all().exclude(user=request.user).exclude(user__in=userlist)
    search = request.GET.get('search')
    if search is not None:
        print(search)
        users = UserProfile.objects.filter(Q(user__username__icontains=search) | Q(user__first_name__icontains=search) | Q(user__last_name__icontains=search)).exclude(user=request.user)
    isProfile = False
    if UserProfile.objects.filter(user=request.user).exists():
        isProfile = True
    context = {"users": users, "isProfile": isProfile}
    print(context)
    return render(request, 'home.html', context)

@login_required(login_url="/")
def view_requests(request):
    followers = Followers.objects.filter(sender=request.user, approved=False)
    context = {"followers": followers}
    print(context, "requests")
    return render(request, 'followers.html', context)

@login_required(login_url="/")
def view_followers_list(request):
    followers = Followers.objects.filter(approved=True).filter(Q(profile__user=request.user) | Q(sender=request.user))
    context = {"followers": followers}
    print(context)
    return render(request, 'followers_list.html', context)

@login_required(login_url="/")
def follow_unfollow(request, username):
    res = Followers.objects.filter(profile__user=request.user, sender__username=username)
    ress = Followers.objects.filter(profile__user__username=username, sender=request.user)

    if res.exists():
        res.delete()
    elif ress.exists():
        ress.delete()
    else:
        profile = UserProfile.objects.get(user=request.user)
        sender = User.objects.get(username=username)
        Followers.objects.create(profile=profile, sender=sender)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/")
def update_profile(request):
    form = UserProfileForm()
    if UserProfile.objects.filter(user=request.user).exists():
            userprofile = UserProfile.objects.get(user=request.user)
            form = UserProfileForm(instance=userprofile)
    if request.method == 'POST':
        if UserProfile.objects.filter(user=request.user).exists():
            userprofile = UserProfile.objects.get(user=request.user)
            form = UserProfileForm(instance=userprofile)
            if form.is_valid():
                form.save()
                return redirect('update-profile')

        form = UserProfileForm(request.POST)
        if form.is_valid():
            frm = form.save(commit=False)
            frm.user = request.user
            frm.save()
            return redirect('update-profile')

    context = {"form": form}
    return render(request, 'update-profile.html', context)

@login_required(login_url="/")
def view_profile(request, username):
    print("yes")
    if request.method == 'POST':
        
        form = UploadPhoto(request.POST, request.FILES)
        
        if form.is_valid():
            frm = form.save(commit=False)
            frm.profile = UserProfile.objects.get(user=request.user)
            frm.save()
        else:
            print("error")
            messages.error(request, "some error")
        
    if not UserProfile.objects.filter(user=request.user).exists():
        return redirect('update-profile')
    obj = UserProfile.objects.get(user__username=username)
    res = Followers.objects.filter(profile__user=request.user, sender__username=username)
    ress = Followers.objects.filter(profile__user__username=username, sender=request.user)
    follow = "no"
    if res.exists():
        follow = "pending"
        if res[0].approved == True:
            follow = "yes"
    elif ress.exists():
        follow = "waiting"
        if ress[0].approved == True:
            follow = "yes"
    photos = Photos.objects.filter(profile__user__username=username)

    form = UploadPhoto()
    
    context = {"profile": obj,
               "following": follow,
               "photos": photos,
               "form": form}
    return render(request, 'profile.html', context)

@login_required(login_url="/")
def accept_request(request, username):
    a = Followers.objects.filter(profile__user__username=username, sender=request.user)
    a.update(approved=True)
    return redirect(request.META.get('HTTP_REFERER'))
