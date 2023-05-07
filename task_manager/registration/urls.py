from django.urls import path
from django.conf.urls.static import static

from task_manager import settings
from registration.views import index, SignUpView, LoginView

app_name = 'registration'


urlpatterns = [
    path('', index, name='start_page'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)