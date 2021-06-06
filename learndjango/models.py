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
    print(f"user with {instance.username} name saved!!!!!")


@receiver(pre_save, sender=User)
def user_pre_save(*args, **kwargs):
    instance = kwargs["instance"]
    print(f"user with {instance.username} name will save............")


@receiver(pre_delete, sender=User)
def user_pre_delete(instance, *args, **kwargs):
    print(f"user with {instance.username} name will be delete............")
    print(" <<<<backup data>>>>")


@receiver(post_delete, sender=User)
def user_post_delete(instance, *args, **kwargs):
    print(f"user with {instance.username} name deleted!!!")


# middleware


class Device(models.Model):
    name = models.CharField(max_length=50, unique=True)
    count = models.PositiveIntegerField()
