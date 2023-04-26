from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from task_manager import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('registration.urls')),
    path('', include('main_page.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)