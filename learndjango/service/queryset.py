from django.db.models import Q, F, Count

from learndjango.models import School, Student, Teacher


def learning_queryset():
    bk=School.objects.create(name="Bach Khoa",address="Hoa Khanh")
    sp=School(name="Su Pham",address="Hoa Khanh")
    sp.save()
    nn=School(name="Ngoai Ngu",address="Hai CHau")
    nn.save()
    Student.objects.bulk_create((Student(name="luan",years=1997,School=bk),
                                Student(name="Hoang",years=1997,School=bk),
                                Student(name="Long",years=2000,School=bk),
                                Student(name="Loan",years=1997,School=nn)))
    luan=Student.objects.get(name="Luan")
    hoang=Student.objects.get(name="Hoang")
    loan=Student.objects.get(name="Loan")
    long=Student.objects.get(name="Long")
    thao=Teacher.objects.create(name="Thao",email="Thao@gmail.com",)
    thao.students.set([luan,hoang,loan])

    print("2 student in all:", Student.objects.all()[:2])
    print("Student with age <97 :", Student.objects.filter(years__gt=1997))
    print("student name start with 'l':", Student.objects.filter(name__startswith="l"))
    print("student name contain with 'o':", Student.objects.filter(name__contains="o"))
    print("student of BK:", Student.objects.filter(School__address="Hoa Khanh"))
    s = Student.objects.filter(Q(years=1997) & Q(name__startswith="l"))
    print("student year equal 1997 and name start 'l'", list(s))
    # using exclude
    print("all student exlcude Luan student:", Student.objects.exclude(name="Luan"))
    # using annotate
    t = Teacher.objects.annotate(student_count=Count(Student))
    print("student count of thao teacher:", t[0].student_count)
    # get all student with order by=name
    print("all student with order by=name:", Student.objects.all().order_by("name"))
    # get all thao teacher info with values
    # print("thao information:", Teacher.objects.get(name="Thao").values())
    # get all student name with values_list
    print("all student name:", Student.objects.values_list("name", flat=True))
    # using select_relative
    luan = Student.objects.select_related("School").get(name="Luan")
    print("School of luan student ", luan.School.name)
