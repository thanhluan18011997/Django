from rest_framework import serializers

from .models import *


class SimpleSchoolSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    address = serializers.CharField(max_length=100)

    def create(self, validated_data):
        if self.is_valid(raise_exception=True):
            return School.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if self.is_valid(raise_exception=True):
            School.objects.filter(name=instance.name).update(**validated_data)
            return School.objects.get(name=instance.name)


class StudentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        read_only_field = ("SChool",)

    def create(self, validated_data):
        print(validated_data)
        if self.is_valid(raise_exception=True):
            instance = Student.objects.create(**validated_data)
            return instance


# authentication

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    name = serializers.CharField()


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=255)
