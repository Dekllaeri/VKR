from django.urls import path
from .views import *


urlpatterns = [
    path('auth/login', CustomTokenCreateView.as_view(), name='custom_login'),
    path('auth/logout', CustomTokenDestroyView.as_view(), name='custom_logout'),
    path('info', UserInfoView.as_view(), name='user-info'),
]
