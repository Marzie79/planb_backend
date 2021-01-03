from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('user-projects', UserProjectView)
# router.register(r'user-project/filter', StatusUserProjectView)
router.register('projects', ProjectView)

urlpatterns = [
    path('projects/<str:slug>/members/', ProjectTeam.as_view({'get': 'list', 'patch': 'update'})),
]

urlpatterns += router.urls
