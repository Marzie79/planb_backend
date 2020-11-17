from django.urls import path
from .views import *

urlpatterns = [
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('user/verify/', VerifyAccount.as_view({'get': 'list', 'post': 'create'})),
    path('user/logout/', Logout.as_view(), name='logout'),
    path('user/signup/', SignUp.as_view(), name='signup'),
    path('user/signin/', MyTokenObtainPairView.as_view()),
    path('user/reset-password/', ResetPassword.as_view()),
    path('list/cities/', SearchCity.as_view()),
    path('list/provinces/', SearchProvince.as_view()),
    path('list/universities/', SearchUniversity.as_view()),
    path('profile/', ProfileUser.as_view({'get': 'retrieve', 'put': 'update'}),
         name='auth_profile'),
]
