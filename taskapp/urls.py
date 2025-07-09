from django.urls import path
from .views import SignupView,LoginView,DashboardView, ModifyTask
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
 

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup-page'), 
    path('login/', LoginView.as_view(),name="login-page"),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('modify/<int:id>',ModifyTask.as_view(),name="update or deletion"),
]