from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .models import School, Student, Teacher


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
