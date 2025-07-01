from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import User
from .serializer import UserSerializer
# Create your views here.
class SignupView(APIView):
    
    def get(self, request):
        return render(request, 'taskapp/signup.html')
    
    def post(self,request):
        serializer= UserSerializer(data =request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"User created successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
