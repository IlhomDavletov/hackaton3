from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import MyUser
from account.serializers import RegistrationSerializer, CustomLoginSerializer


class RegistrationView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            print('hello view')
            return Response('Successfully registered', status=status.HTTP_201_CREATED)

        return Response('Not Valid', status=status.HTTP_400_BAD_REQUEST)

class ActivationView(APIView):
    def get(self,request, activation_code):
        user = get_object_or_404(MyUser, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Successfully activated!', status=status.HTTP_200_OK)

class LoginView(ObtainAuthToken):
    serializer_class = CustomLoginSerializer