from django.urls import path, include
from rest_framework_nested import routers
from .views import *
from .views.view_user import *

router = routers.SimpleRouter()
router.register('user', UserInfoView,)

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
        path('brief-profile/', BriefProfileUser.as_view({'get': 'retrieve'}), name='brief_profile'),
        path('profile/', include([
            path('', ProfileUser.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='profile'),
            path('avatar/',
                 ProfilePicture.as_view({'get': 'retrieve', 'post': 'partial_update', }, name='profile_picture')),
            path('resume/',
                 ProfileResume.as_view({'get': 'retrieve', 'post': 'partial_update', 'delete': 'destroy', }, name='profile_resome')),
            path('skills/', UserSkill.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name="skills"),
        ])),

    ])),
    path('', include(router.urls)),
    path('list/', include([
        path('cities/', SearchCity.as_view()),
        path('provinces/', SearchProvince.as_view()),
        path('universities/', SearchUniversity.as_view()),
        path('skills/', SearchSkill.as_view()),
    ])),
]
