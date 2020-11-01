from django.urls import path
from .views import *

urlpatterns = [
    path('validate-email/', ValidateEmail.as_view({'get': 'list', 'post': 'create'})),
    path('sign-up/', SignUp.as_view()),
    path('sign-in/', MyTokenObtainPairView.as_view()),
    path('request-reset-password/', RequestResetPassword.as_view()),
    path('reset-password/', ResetPassword.as_view()),
    # path('account/', GoogleView.as_view()),
]
