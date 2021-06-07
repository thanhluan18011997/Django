import random
import string
from datetime import datetime, timedelta

import jwt
from django.contrib.auth import authenticate
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from learndjango.authentication import Authentication
from .serializers import *
from .serializers import LoginSerializer, RegisterSerializer, RefreshSerializer


# Create your views
def test_function_view(request):
    thao = Teacher.objects.get(name="Thao")
    student_list = thao.students.all()
    context = {"thao": thao, "student_list": student_list}
    return render(request, "functionview.html", context=context)


class test_class_base_view(View):

    def get(self, request, *args, **kwargs):
        bk = School.objects.get(name="Bach Khoa")
        student_list = bk.students.all()
        context = {"bk": bk, "student_list": student_list}
        return render(request, "classbaseview.html", context=context)


# serializer


class using_simple_school_serrializer(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, name, *args, **kwargs):
        print(name)
        school = School.objects.get(name=name)
        print(school)
        serializer = SimpleSchoolSerializer(school)
        print(serializer.data)
        return JsonResponse(data=serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = SimpleSchoolSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(data=serializer.data)
        return JsonResponse({"status": "error"})

    def put(self, request, name, *args, **kwargs):
        try:
            instance = School.objects.get(name=name)
        except Exception as e:
            return JsonResponse({"status": "invalid"})
        serializer = SimpleSchoolSerializer(data=request.data, instance=instance)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return JsonResponse(serializer.data)


class using_school_model_serrializer(APIView):
    def get(self, request, id, *args, **kwargs):
        student = Student.objects.get(pk=id)
        print(student)
        serializer = StudentModelSerializer(student)
        print(serializer.data)
        return JsonResponse(data=serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = StudentModelSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(data=serializer.data)
        return JsonResponse({"status": "error"})


# usiing viewset

class using_viewset(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SimpleSchoolSerializer


def create_access_token(info):
    token= jwt.encode(
        {"exp": datetime.now() + timedelta(minutes=7), **info},
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    return token

def create_refresh_token():
    token=jwt.encode(
        {"exp": datetime.now() + timedelta(days=100), "data": "".join(random.choices(string.ascii_lowercase+string.digits,k=8))},
        settings.SECRET_KEY,
        algorithm="HS256")
    return token


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password'])

        if not user:
            return Response({"error": "Invalid "}, status="400")

        Jwt.objects.filter(user_id=user.id).delete()

        access = create_access_token({"user_id": user.id})
        refresh = create_refresh_token()

        Jwt.objects.create(
            user_id=user.id, access=access, refresh=refresh
        )

        return Response({"access": access, "refresh": refresh})


class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        CustomUser.objects._create_user(**serializer.validated_data)

        return Response({"success": "User created."})


class RefreshView(APIView):

    def post(self, request):
        serializer = RefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            current_jwt = Jwt.objects.get(
                refresh=serializer.validated_data["refresh"])
        except Jwt.DoesNotExist:
            return Response({"error": "refresh token not found"}, status="400")
        if not Authentication.verify_token(serializer.validated_data["refresh"]):
            return Response({"error": "Token is invalid or has expired"})

        access = create_access_token({"user_id": current_jwt.user.id})
        refresh = create_refresh_token()

        current_jwt.access = access
        current_jwt.refresh = refresh
        current_jwt.save()

        return Response({"access": access, "refresh": refresh})

