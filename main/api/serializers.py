from rest_framework import serializers
from main.models import *


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'


class ToDoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoList
        fields = '__all__'
        depth = 1


class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = '__all__'


class UserLoginSerializer(serializers.ModelSerializer):
    active_organization = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['email', 'password', 'active_organization']


class OrganizationCreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ('pk', )


class UserRegisterSerializer(serializers.ModelSerializer):
    organizations = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'organizations']
