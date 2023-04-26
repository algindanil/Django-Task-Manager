from django.urls import path

from registration.views import index, SignUpView, LoginView


app_name = 'registration'


urlpatterns = [
    path('', index, name='start_page'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]