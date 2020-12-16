from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'user-project', UserProject)
urlpatterns = router.urls
