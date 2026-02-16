from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from .serializers import UserCreateSerializer, UserAuthSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random
from rest_framework.views import APIView

class AuthAPIView(APIView):
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # username = serializer.validated_data['username']
        # password = serializer.validated_data['password']

        user = authenticate(**serializer.validated_data)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            
            return Response(data={"key" : token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def registration_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']



    user = User.objects.create_user(username=username, password=password, is_active=False)

    return Response(status=status.HTTP_201_CREATED,
                    data={'user_id': user.id})

