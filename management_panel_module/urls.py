from django.urls import path
from . import views

urlpatterns = [
    path('', views.ManagementPanelView.as_view(), name='management_panel_page'),
    path('students-list', views.StudentsListView.as_view(), name='students_list_page'),
    path('set-homework', views.SetHomeWorkView.as_view(), name='set_homework_page'),
]
