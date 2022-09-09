from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationList.as_view(), name='notification_list'),
    path('new', views.CreateNotification.as_view(), name='create_notification'),
    path('<pk>/update', views.UpdateNotification.as_view(), name='update_notification'),
]
