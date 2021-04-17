from django.urls import path, include
from rest_framework_nested import routers

from .views import *
from .views.view_message import MessageView
from .views.view_notification import NotificationView
from .views.view_project import ProjectView
from .views.view_project_team import ProjectTeam
from .views.view_user_info import UserInfoView, UserInfoProjectView
from .views.view_user_project import UserProjectView

router = routers.SimpleRouter()
router.register("projects", ProjectView)
router.register("users", UserInfoView)
router.register("messages", MessageView)
router.register("notifications", NotificationView)

project_router = routers.NestedSimpleRouter(router, "projects", lookup="slug")
project_router.register("members", ProjectTeam, basename="domain")

user_router = routers.NestedSimpleRouter(router, "users", lookup="slug")
user_router.register("projects", UserInfoProjectView, basename="domain")

urlpatterns = [
    path('user-projects/', UserProjectView.as_view()),
    path('', include(router.urls)),
    path('', include(user_router.urls)),
    path('', include(project_router.urls)),

]