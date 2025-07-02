from django.urls import path
from .views import SignupView,LoginView,DashboardView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
 

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup-page'), 
    path('login/', LoginView.as_view(),name="login-page"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]