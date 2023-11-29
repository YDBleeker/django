from django.urls import path
from .views import helloworld, index, wifi, setting, get_wifi_networks, connect_to_wifi, reboot, uuid, emotion

urlpatterns = [
    path('hello/', helloworld, name='helloworld'),
    path('index/', index, name='index'),
    path('wifi/', wifi, name='wifi'),
    path('wifi/get_networks/', get_wifi_networks, name='get_wifi_networks'),
    path('wifi/connect', connect_to_wifi, name='connect_to_wifi'),
    path('settings/', setting, name='setting'),
    path('reboot/', reboot, name='reboot'),
    path('uuid/', uuid, name='uuid'),
    path('emotion/', emotion, name='emotion'),
]