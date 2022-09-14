from django.urls import path
from . import views

urlpatterns = [
    path('', views.PollList.as_view(), name='poll_list'),
    path('new', views.CreatePoll.as_view(), name='create_poll'),
    path('<pk>/update', views.UpdatePoll.as_view(), name='update_poll'),
    path('<pk>/delete', views.DeletePoll.as_view(), name='delete_poll'),
    path('<pk>/vote', views.VotePoll.as_view(), name='vote_poll'),
    path('<pk>/option/new', views.add_poll_option, name='add_poll_option'),
    path('<pk>/option/<id>/update', views.update_poll_option, name='update_poll_option'),
    path('<pk>/option/<id>/delete', views.delete_poll_option, name='delete_poll_option'),
]
