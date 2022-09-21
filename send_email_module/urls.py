from django.urls import path
from . import views


urlpatterns = [
    path('', views.SendEmail.as_view(), name='send_email'),
    path('list', views.EmailList.as_view(), name='email_list')
]