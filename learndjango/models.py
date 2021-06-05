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
