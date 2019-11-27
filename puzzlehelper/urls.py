from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('codes.urls')),
    path('tools/', include('tools.urls')),
    path('admin/', admin.site.urls),
]
