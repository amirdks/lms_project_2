from django.urls import path

from chat_module import views

urlpatterns = [
    path('', views.ChatView.as_view(), name='chat_box_view'),
    path('<str:chat_id>/', views.ChatView.as_view(), name='chat_contact_view'),
]
