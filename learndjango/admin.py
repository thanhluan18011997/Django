from django.contrib import admin
from .models import School,Teacher,Student,CustomUser
from .models import Jwt

# Register your models here.
admin.site.register((School,Teacher,Student,CustomUser,Jwt))


