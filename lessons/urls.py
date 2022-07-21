from django.urls import path
from . import views

urlpatterns = [
    path('', views.LessonsList.as_view(), name='lessons_list_page'),
    path('<int:id>', views.ListHomeWorks.as_view(), name='list_home_works'),
    path('<int:id>/<int:pk>', views.HomeWorkView.as_view(), name='home_work_page'),
    path('<int:lesson>/new', views.SetHomeWorkView.as_view(), name='set_new_home_work_lesson'),
    path('<int:id>/<slug:slug>/students-score', views.StudentListHomeWorks.as_view(), name='students-list-home-works'),
    path('<int:id>/<slug:slug>/students-score/<int:user_id>', views.StudentLIstSentHomeWorks.as_view(),
         name='student-list-sent-home-works'),
    path('<int:id>/<int:pk>/delete', views.DeleteHomeWorkView.as_view(), name='delete_home_work'),
    path('<int:id>/<int:pk>/delete-home-work', views.DeleteSentHomeWorkView.as_view(), name='delete_sent_home_work'),
    path('<int:id>/<int:pk>/edit', views.EditHomeWorkView.as_view(), name='edit_home_work'),
    path('<int:id>/<int:pk>/home-works-list', views.ListSentHomeWorks.as_view(), name='list-sent-home-works'),
]
