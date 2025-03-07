"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.utils.translation import gettext_lazy as _


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # set_language URL-sini qo‘shish
]

urlpatterns += i18n_patterns(
    path(_(''), include('blog.urls')),  # Asosiy app uchun URL-lar
    path(_('accounts/'), include('accounts.urls')),  # Accounts app URL-lari
    path(_('ckeditor/'), include('ckeditor_uploader.urls')),
    path(_('admin/'), admin.site.urls)
,  # Shop app URL-lari
    # Yana boshqa app URL-larini shu yerda qo‘shish mumkin
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)