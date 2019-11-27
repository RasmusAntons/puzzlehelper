from django.urls import path
from django.conf.urls import include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('barcodes/', views.barcodes_index, name='barcodes'),
    path('barcodes/<short>/edit', views.barcodes_edit, name='barcodes_edit'),
    path('img/<filename>', views.img, name='img')
]
