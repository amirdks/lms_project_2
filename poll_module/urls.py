from django.urls import path
from . import views

urlpatterns = [
    path('new', views.CreatePoll.as_view(), name='create_poll'),
    # path('<pk>/options', views.CreatePoll.as_view(), name='create_poll'),
    path('<pk>/update', views.UpdatePoll.as_view(), name='update_poll'),
]
