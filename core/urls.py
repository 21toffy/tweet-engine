from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.urls.conf import include
from django.conf.urls.static import static
from django.conf.urls import handler404
from rest_framework import routers
from rest_framework_simplejwt.views import TokenVerifyView
from django.urls import re_path
from django.views.static import serve

from Auth.views import custom_404_handler


def trigger_error(request):
    division_by_zero = 1 / 0



urlpatterns = [
    path("admin/", admin.site.urls),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
handler404 = custom_404_handler  # noqa
