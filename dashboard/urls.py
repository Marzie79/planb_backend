from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('user-projects', UserProjectView)
# router.register(r'user-project/filter', StatusUserProjectView)
router.register('projects', ProjectView)


urlpatterns = router.urls
