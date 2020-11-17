from django.urls import path
from .views import *

urlpatterns = [
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('validate-email/', ValidateEmail.as_view({'get': 'list', 'post': 'create'})),
    path('logout/',Logout.as_view(),name='logout'),
    path('sign-up/', SignUp.as_view()),
    path('sign-in/', MyTokenObtainPairView.as_view()),
    path('request-reset-password/', RequestResetPassword.as_view()),
    path('reset-password/', ResetPassword.as_view()),
    path('cities/', SearchCity.as_view()),
    path('provinces/', SearchProvince.as_view()),
    path('universities/', SearchUniversity.as_view()),
    path('profile/', ProfileUser.as_view({'get': 'retrieve', 'put': 'update'}),
         name='auth_profile'),
]
