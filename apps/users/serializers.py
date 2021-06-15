from rest_framework import serializers
from .models import *


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = (
            "email",
            "verified",
            "date_joined",
            "is_active",
            'first_name',
            'is_superuser',
            'last_name',
            'is_staff',
            'password',
            'user_permissions',
            'groups',
            'last_login'
        )
        model = User

class PendingUserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = "verified",
        model = PendingUser


class UserPartialSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('contacts',)
        model = User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    contacts = UserCreateSerializer(required=False, many=True)
    class Meta:
        exclude = (
            "email",
            'is_superuser',
            "date_joined",
            "is_active",
            'last_name',
            'first_name',
            'is_staff',
            'password',
            'user_permissions',
            'groups',
            'last_login'
        )
        model = User


class GetUserSerializer(serializers.ModelSerializer):

    contacts = UserSerializer(required=False, many=True)
    class Meta:
        exclude = (
            "email",
            'is_superuser',
            "date_joined",
            "is_active",
            'last_name',
            'first_name',
            'is_staff', 
            'password',
            'user_permissions',
            'groups',
            
            'last_login'
        )
        model = User

class ShortUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'pk',
            'username',
            'image',
            'fio',
            'verified'
        )
        model = User
