from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import User ,Task
from .serializer import UserSerializer, TaskSerializer
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
import requests



# Create your views here.
class SignupView(APIView):
        
    def post(self,request):
        serializer= UserSerializer(data =request.data, context ={"mode":"signup"})
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"200","message":"Signup Succsessful"})
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class LoginView(APIView):
     def post(self,request):
        serializer= UserSerializer(data =request.data, context ={"mode":"login"})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            request.session['access_token'] = access_token
            request.session['username'] = user.email

            print("Login Successful")

            response = Response({
                "status": 202,
                "message": "Login Successful",
                "username" : user.email,
                "is_superuser" : user.is_superuser,
            }, status=status.HTTP_202_ACCEPTED)

            # Adding token to headers for use in frontend JS or Postman)
            response['Authorization'] = f'Bearer {access_token}'

            return response
        
        print("Serializer Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class DashboardView(APIView):
    def get(self, request):
        tasks = Task.objects.filter(userid=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    
    def post(self,request):
        data = request.data
        
        serializer = TaskSerializer(data = data, context={'request': request})  #using context to send all the request data 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ModifyTask(APIView):
    def put (self,request,id):
        try :
            task = Task.objects.get(id=id,userid =request.user)    #checking if the task exists or not
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=404)
    
        serializer = TaskSerializer(task,data= request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400) 

    def delete (self,request,id):
        try :
            task = Task.objects.filter(id=id).delete()
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=404)              
 
        return Response({"message":"Task deleted successfully"},status=status.HTTP_200_OK)
    


            
     