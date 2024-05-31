from ctypes import cast
from math import fabs
from typing import Iterable
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Religions(models.Model):
    religion = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.religion
    def save(self):
        self.religion = self.religion.capitalize()
        return super().save()

class Caste(models.Model):
    caste = models.CharField(max_length=50)
    religion = models.ForeignKey(Religions, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.caste
    def save(self):
        self.caste = self.caste.capitalize()
        return super().save()


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    avatar = models.ImageField(upload_to='media', default='defaultprofile.jpg')
    bio = models.CharField(max_length=250, default="Hey Peeps, I'm Here!")
    caste = models.ForeignKey(Caste, on_delete=models.CASCADE)
    height = models.CharField(max_length=5)
    weight = models.CharField(max_length=5)
    interest = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.first_name


class Followers(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)


class Photos(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='media', blank=False, null=False)
