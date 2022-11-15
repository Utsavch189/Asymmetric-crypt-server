from django.urls import path
from .views import *

urlpatterns = [
    path('send',send),
    path('getAction',getAction),
    path('getKey',getPrivateKey),
    path('getSystemInfo',getSystemInfo)
]