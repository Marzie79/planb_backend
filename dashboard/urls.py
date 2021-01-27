from django.urls import path, include
from rest_framework_nested import routers

from .views import *

router = routers.SimpleRouter()
router.register('projects', ProjectView)
router.register('users', UserInfoView)

domains_router = routers.NestedSimpleRouter(router, 'projects', lookup='slug')
domains_router.register('members', ProjectTeam, basename='domain')

urlpatterns = [
    path('user-projects/', UserProjectView.as_view()),
    path('', include(router.urls)),
    path('', include(domains_router.urls)),
]
