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
                "access_token": access_token,
                "refresh_token": str(refresh)
            }, status=status.HTTP_202_ACCEPTED)

            # Adding token to headers for use in frontend JS or Postman)
            response['Authorization'] = f'Bearer {access_token}'

            return response
        
        print("Serializer Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class DashboardView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_header(self,request):
        username = request.session.get('username')
        token = request.session.get('access_token')


        if not token:
            return redirect('login')
            
        
        headers ={
            "Authorization" : f"Bearer {token}"
        }
        return token, headers


    def get(self, request):
        import pdb;pdb.set_trace()
        username = request.session.get('username')
        token, headers = self.get_header(request)
        try:
            # Task.objects.filter(user)
            response = requests.get("http://127.0.0.1:8000/tasks/api/tasks/", headers=headers)
            print(f"Response status: {response.status_code}")  # Debug print
            print(f"Response content: {response.content}")     # Debug print
            
            if response.status_code == 200:
                tasks = response.json()
                print(f"Tasks received: {tasks}")  # Debug print
            else:
                print(f"API Error: {response.status_code}")
                tasks = []
        except Exception as e:
            print(f"Exception occurred: {str(e)}")  # Debug print
            tasks = []

        return render(request, "taskapp/dashboard.html", {
            'username': username, 
            'token': token, 
            'tasks': tasks
        }) 
    
    def post(self,request):
        token, headers = self.get_header(request)
        data = {
        "task": request.POST.get("task"),
        "details": request.POST.get("details"),
        "start_date": request.POST.get("start_date"),
        "deadline": request.POST.get("deadline"),
        "progress": request.POST.get("progress"),
        "category": request.POST.get("category")
    }

        response = requests.post("http://127.0.0.1:8000/tasks/api/tasks/", headers=headers, data=data)

        if response.status_code == 201:
            return redirect('dashboard')
        else:
            return self.get(request) 





    
class TaskAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        import pdb;pdb.set_trace();
        user= request.user
        tasks = Task.objects.filter(userid=user)
        serializer = TaskSerializer(tasks,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TaskSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
   


            
     