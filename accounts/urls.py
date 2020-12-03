from django.urls import path
from .views.view_list import *
from .views.view_token import *
from .views.view_token import *
from .views.view_signup import *
from .views.view_profile import *

urlpatterns = [
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('user/verify/', VerifyAccount.as_view({'get': 'retrieve', 'post': 'create'}), name='verify'),
    path('user/logout/', Logout.as_view(), name='logout'),
    path('user/signup/', SignUp.as_view(), name='signup'),
    path('user/signin/', MyTokenObtainPairView.as_view()),
    path('user/reset-password/', ResetPassword.as_view({'patch': 'partial_update', 'post': 'create'}), name='reset_password'),
    path('list/cities/', SearchCity.as_view()),
    path('list/provinces/', SearchProvince.as_view()),
    path('list/universities/', SearchUniversity.as_view()),
    path('profile/', ProfileUser.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='auth_profile'),
]
