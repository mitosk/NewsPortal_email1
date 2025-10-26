from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),  # все маршруты из news/urls.py
    path('accounts/', include('allauth.urls')),  # allauth маршруты
]
