from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='RESTMart E-commerce API',
        default_version='v1',
        description='API docmentation for RESTMart E-commerce project',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@restmart.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,), # Allows all the users to views the doc
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-ui'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json' )
] + debug_toolbar_urls()
