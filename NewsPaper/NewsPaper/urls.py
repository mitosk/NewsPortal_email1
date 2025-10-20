from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('about/', RedirectView.as_view(url='/news/', permanent=True)),
    path('', RedirectView.as_view(url='/news/', permanent=True)),
]