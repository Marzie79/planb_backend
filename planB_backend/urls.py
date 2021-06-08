from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from accounts.views import *
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="planB API",
        default_version='v1',
        description="Plan",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)
class Apps(Enum):
    USERS = ''
    DASHBORAD = 'dashboard/'

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path(Apps.USERS.value, include('accounts.urls')),
                  path(Apps.DASHBORAD.value, include('dashboard.urls')),
                  # comment versioning
                  # comment versioning
                  #      path('api/v1/', include((v1, 'v1'), namespace='v1')),
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                  path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
