from django.urls import path, include
from .views import *

urlpatterns = [
    path('user/profile/', include([
        path('skill/', UserSkill.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name="skills"),
    ])),
]
