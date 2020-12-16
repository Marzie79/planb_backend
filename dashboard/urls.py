from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'user-project', UserProjectView)
urlpatterns = router.urls
