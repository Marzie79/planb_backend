from django.urls import path, include
from .views.view_list import *
from .views.view_token import *
from .views.view_token import *
from .views.view_signup import *
from .views.view_profile import ProfilePicture, ProfileUser

urlpatterns = [
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('user/', include([
        path('verify/', VerifyAccount.as_view({'get': 'retrieve', 'post': 'create'}), name='verify'),
        path('logout/', Logout.as_view(), name='logout'),
        path('signup/', SignUp.as_view(), name='signup'),
        path('signin/', MyTokenObtainPairView.as_view()),
        path('reset-password/', ResetPassword.as_view({'patch': 'partial_update', 'post': 'create'}),
             name='reset_password'),
    ])),
    path('list/', include([
        path('cities/', SearchCity.as_view()),
        path('provinces/', SearchProvince.as_view()),
        path('universities/', SearchUniversity.as_view()),
        path('skills/', SearchSkill.as_view()),
    ])),

    path('profile/', ProfileUser.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='auth_profile'),
    path('profile/picture', ProfilePicture.as_view({'post': 'partial_update',}),)
]
