from django.urls import path

from chat_module import views

urlpatterns = [
    path('', views.ChatList.as_view(), name='chat_box_view'),
    path('<str:username>/', views.ChatPv.as_view(), name='chat_pv_view'),
]
