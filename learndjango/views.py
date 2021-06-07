from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import School, Student, Teacher
from .serializers import *


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
