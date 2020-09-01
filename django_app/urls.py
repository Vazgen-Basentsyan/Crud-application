"""django_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

from users.views import UserViewSet, HomeViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'homes', HomeViewSet)

urlpatterns = [
    path('', include("users.urls")),
    url(r'^admin/', admin.site.urls),
    path('api/v0/', include(router.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

