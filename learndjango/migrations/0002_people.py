# Generated by Django 3.2.4 on 2021-06-05 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learndjango', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('balance', models.PositiveIntegerField()),
            ],
        ),
    ]
