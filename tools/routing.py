from django.urls import path

from . import consumers

ws_urlfinder = [
    path('ws/urlfinder/', consumers.UrlfinderConsumer),
]