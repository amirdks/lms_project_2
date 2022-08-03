from django.urls import path
from . import views

urlpatterns = [
    path('students-list', views.StudentsListView.as_view(), name='students_list_page'),
    path('students-list-search', views.search_student_list, name='students_list_search'),
    path('set-homework', views.SetHomeWorkView.as_view(), name='set_homework_page'),
]
