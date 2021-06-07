from django.db import models


# Create your models here.


class School(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    years = models.PositiveIntegerField()
    School = models.ForeignKey(School, on_delete=models.CASCADE, related_name="students")

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    email = models.EmailField(max_length=40)
    students = models.ManyToManyField(Student, related_name="teachers")

    def __str__(self):
        return self.name


class People(models.Model):
    name = models.CharField(max_length=50)
    balance = models.PositiveIntegerField()


# signal
from django.conf import settings

from django.dispatch import receiver
from django.db.models.signals import (pre_save,
                                      post_save,
                                      pre_delete,
                                      post_delete,
                                      )

User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def user_post_save(*args, **kwargs):
    instance = kwargs["instance"]
    print(f"user with {instance} name saved!!!!!")


@receiver(pre_save, sender=User)
def user_pre_save(*args, **kwargs):
    instance = kwargs["instance"]
    print(f"user with {instance} name will save............")


@receiver(pre_delete, sender=User)
def user_pre_delete(instance, *args, **kwargs):
    print(f"user with {instance} name will be delete............")
    print(" <<<<backup data>>>>")


@receiver(post_delete, sender=User)
def user_post_delete(instance, *args, **kwargs):
    print(f"user with {instance} name deleted!!!")


# middleware


class Device(models.Model):
    name = models.CharField(max_length=50, unique=True)
    count = models.PositiveIntegerField()


# Customize user and Authentication
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Require email!!!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('name', "admin")

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    def __str__(self):
        return self.email


# authen


class Jwt(models.Model):
    user = models.OneToOneField(
        CustomUser, parent_link=True, on_delete=models.CASCADE)
    access = models.TextField()
    refresh = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
