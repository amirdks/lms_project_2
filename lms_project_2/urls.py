"""lms_project_2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include
from management_panel_module.views import InfoAdminView

urlpatterns = [
                  path('', include('home_module.urls')),
                  path('', include('account_module.urls')),
                  path('lessons/', include('lessons.urls')),
                  path('notifications/', include('notification_module.urls')),
                  path('', include('management_panel_module.urls')),
                  path('poll/', include('poll_module.urls')),
                  path('admin/', admin.site.urls, name='admin_info_page'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'home_module.views.not_found'
