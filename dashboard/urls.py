from django.urls import path, include
from .views import *

urlpatterns = [
    path('skill/', include([
        path('child-skills/<int:current_skill_id>/', ChildSkill.as_view({'get': 'list'}), name="child-skills"),
        path('my-skills', UserSkill.as_view({'get': 'list'}), name="my-skills"),
    ])),
]
