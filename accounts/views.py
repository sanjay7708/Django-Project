from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_protect
from django.middleware.csrf import get_token
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
# Create your views here.

def csrf_token(request):
    return JsonResponse({"csrf_token":get_token(request)})

class LoginView(APIView):
    def post(self,request):
        data=request.data
        username=data.get("username")
        password=data.get("password")
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return Response({'message':"logged In"},status=status.HTTP_200_OK)
        return Response({'message':"invalid credentials"},status=status.HTTP_401_UNAUTHORIZED)
class SignUpView(APIView):
    def post(self,request):
        data=request.data
        username=data.get("username")
        email=data.get('email')
        password=data.get('password')
        confirm_password=data.get('confirm_password')
        
        if not all([username,email,password,confirm_password]):
            return Response({'message':"all fields require"},status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'message':"username already registered"},status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'message':'email id already register'},status=status.HTTP_400_BAD_REQUEST)
        if password!=confirm_password:
            return Response({"message":"password doest not match"},status=status.HTTP_400_BAD_REQUEST)
        user=User.objects.create(username=username,email=email)
        user.set_password(password)
        user.save()
        return Response({'message':"New User Registered Sucessfully"},status=status.HTTP_201_CREATED)
class LogoutView(APIView):
    def post(self,request):
        logout(request)
        return Response({"message":"User Logout Sucessfully"},status=status.HTTP_200_OK)

class Whoami(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        return Response({"username":request.user.username},status=status.HTTP_200_OK)
        