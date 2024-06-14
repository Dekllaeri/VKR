from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from backend_config import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls'), name='users'),
    path('api/v1/', include('api_v1.urls'), name='api_v1'),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
