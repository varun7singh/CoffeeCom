from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/',include('watchlist.api.urls')),
    path('auth-admin/',include('rest_framework.urls')),
]
