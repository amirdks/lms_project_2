from django.urls import path
from . import views

urlpatterns = [
    path('user', views.UserPanelView.as_view(), name='user_panel_page'),
    path('user/<int:id>', views.AnotherUserPanelView.as_view(), name='view_another_user_page'),
    path('user/<int:user_id>/start-chat/', views.StartChatView.as_view(), name='start_chat_with_user'),
    path('user/edit-info', views.EditUserInfo.as_view(), name='edit_user_info_page'),
    path('user/edit-pass', views.EditUserPass.as_view(), name='edit_user_pass_page'),
    path('login', views.LoginView.as_view(), name='login_page'),
    path('logout/', views.LogoutView.as_view(), name='logout_page'),
    path('forget-pass', views.ForgetPasswordView.as_view(), name='forget-pass-page'),
    path('reset-pass/<active_code>', views.ResetPasswordView.as_view(), name='reset_pass'),
]
