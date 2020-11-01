from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from accounts.views import MyTokenObtainPairSerializer
from backend import settings
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from accounts.views import *
schema_view = get_schema_view(
    openapi.Info(
        title="Tabesh API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

v1 = [
    path('', include('accounts.urls')),
]

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/v1/', include((v1, 'v1'), namespace='v1')),
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
                  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                  path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
