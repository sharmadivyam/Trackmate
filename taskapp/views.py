from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import User
from .serializer import UserSerializer
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken



# Create your views here.
class SignupView(APIView):
    
    def get(self, request):
            return render(request, "taskapp/signup.html")
        
    def post(self,request):
        serializer= UserSerializer(data =request.data, context ={"mode":"signup"})
        if serializer.is_valid():
            serializer.save()
            return redirect('/tasks/login/')
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class LoginView(APIView):
     def get(self,request):
         return render(request,"taskapp/login.html")
     def post(self,request):
        serializer= UserSerializer(data =request.data, context ={"mode":"login"})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            request.session['access_token'] = access_token
            request.session['username'] = user.email 
            return redirect ('dashboard')
        return render(request,'login.html', {'error':"invalid credentials"})

class DashboardView(APIView):
    def get(self, request):
        username = request.session.get('username')
        token = request.session.get('access_token')
        if not token:
            return redirect('login')
        return render(request, "taskapp/dashboard.html" ,{'username':username ,'token':token})       

   


            
     