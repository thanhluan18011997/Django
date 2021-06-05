from learndjango.models import School, Student, Teacher, People
from django.db import transaction, DatabaseError

# Luan balance have 100$
luan = People.objects.create(name="Luan", balance=100)


def doesnt_using_transaction():
    luan.balance = 100
    # transfer error when send a not found object(Hoa)
    luan.balance -= 50
    luan.save()
    # Hoa does'nt exist
    hoa = People.objects.get(name="Hoa")
    hoa.balance += 50
    hoa.save()

    # transfer error when send a not found object(Hoa) using transaction


def using_transaction():
    luan.balance = 100
    luan.save()
    with transaction.atomic():
        luan.balance -= 50
        luan.save()
        # Hoa does'nt exist
        hoa = People.objects.get(name="Hoa")
        hoa.balance += 50
        hoa.save()
