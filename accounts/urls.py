from django.urls import path, include
from rest_framework_nested import routers
from .views import *

router = routers.SimpleRouter()

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
        path('brief-profile/', BriefProfileUser.as_view({'get': 'retrieve'}), name='profile_brief'),
        path('profile/', include([
            path('', ProfileUser.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='profile'),
            path('avatar/',
                 ProfilePicture.as_view({'get': 'retrieve', 'post': 'partial_update', 'delete': 'destroy', }),
                 name='profile_picture'),
            path('resume/',
                 ProfileResume.as_view({'get': 'retrieve', 'post': 'partial_update', 'delete': 'destroy', }),
                 name='profile_resume'),
            path('skills/', UserSkill.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='profile_skills'),
        ])),

    ])),
    path('', include(router.urls)),
    path('list/', include([
        path('cities/', SearchCity.as_view(), name='list_city'),
        path('provinces/', SearchProvince.as_view(), name='list_province'),
        path('universities/', SearchUniversity.as_view(), name='list_university'),
        path('skills/', SearchSkill.as_view(), name='list_skill'),
    ])),
]
