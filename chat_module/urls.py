from django.urls import path

from chat_module import views

urlpatterns = [
    path('', views.ChatView.as_view(), name='chat_box_view'),
    path('<str:chat_id>/file-upload/', views.FileUploadMessageView.as_view(), name='file_message_view'),
    path('<str:chat_id>/file-download/<str:file_id>', views.FileDownloadMessageView.as_view(), name='file_download_message_view'),
    path('<str:chat_id>/', views.ChatView.as_view(), name='chat_contact_view'),
]
