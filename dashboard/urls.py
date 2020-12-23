from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'user-project', UserProjectView)
# router.register(r'user-project/filter', StatusUserProjectView)
urlpatterns = router.urls
