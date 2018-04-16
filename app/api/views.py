# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework import status, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


from app.db.models import *
from .serializers import *

def index(request):
    html = "<html><body><h1> clean-ws </h1></body></html>"
    return HttpResponse(html)


class LoginService(APIView):

    def post(self, request, format=None):

        username   = request.data['username']
        password   = request.data['password']

        try:
            user = User.objects.get(username=username)
            user = authenticate(username=username, password=password)
            if user is not None:
                # A backend authenticated the credentials
                user_serializer = UserSerializer(user)
                data = user_serializer.data

                #Get token
                try:
                    token = Token.objects.get(user=user)
                except Token.DoesNotExist:
                    token = Token.objects.create(user=user)
                data['token'] = token.key
                return Response({'user': data})

            else:
                # No backend authenticated the credentials
                error = Error(4004, "Error", "El Usuario o Contraseña ingresados son incorrectos.")
                content = {'error':error.serializer()}
                return Response(data=content, status=status.HTTP_400_BAD_REQUEST)
        
        except User.DoesNotExist:
            usuario = None
            error = Error(4005, "Error", "El usuario ingresado aún no se encuentra registrado.")
            content = {'error':error.serializer()}
            return Response(data=content, status=status.HTTP_400_BAD_REQUEST)


class Error:
    def __init__(self, status, title, detail):
        self.status = status
        self.title  = title
        self.detail = detail

    def serializer(self):
        return {'status': self.status, 'title':self.title, 'detail':self.detail}


class RegisterService(APIView):
    def post(self, request, format=None):

        username   = request.data['username']
        password   = request.data['password']

        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            #error = Error(4004, "Error", "El Usuario o Contraseña ingresados son incorrectos.")
            #content = {'error':error.serializer()}
            serialized = RegisterUserSerializer(data=request.data)
            if serialized.is_valid():
                serialized.save()
                
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            error = Error(4000, "Error", "El Usuario ya existe.")
            content = {'error':error.serializer()}
            return Response(data=content, status=status.HTTP_400_BAD_REQUEST)

