from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from common.validators import validate_age

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["birth_date"] = str(user.birth_date)
        return token

class UserBaseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)


class UserAuthSerializer(UserBaseSerializer):
    pass

class UserCreateSerializer(UserBaseSerializer):
    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('User already exists!')
    birth_date = serializers.DateField(required=False, allow_null=True)

    def validate_birth_date(self, birth_date):
        return validate_age(birth_date)
