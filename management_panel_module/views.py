from datetime import timedelta

from django.contrib import messages
from django.contrib.admin import AdminSite
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from online_users.models import OnlineUserActivity

from account_module.models import User
from lesson_module.models import Lesson, SetHomeWork
from management_panel_module.filters import StudentListResultFilter
from management_panel_module.forms import SetHomeWorkForm
from management_panel_module.mixins import JustTeacherMixin
from notification_module.models import Notification, CustomNotification
from utils.time import end_time_calculator


class StudentsListView(LoginRequiredMixin, JustTeacherMixin, View):
    login_url = reverse_lazy('login_page')

    def get(self, request: HttpRequest):
        teacher = request.user
        students = User.objects.filter(is_teacher=False, base__lesson__teacher_id=teacher.id,
                                       field_of_study__lesson__teacher_id=teacher.id).distinct()
        filters = StudentListResultFilter(request.GET, queryset=students)
        # if request.GET.get('base') or request.GET.get('field_of_study'):
        students = filters.qs
        context = {
            'students': students,
            'filter': filters
        }

        return render(request, 'management_panel_module/students_list.html', context)


@login_required()
def search_student_list(request: HttpRequest):
    teacher = request.user
    students = User.objects.filter(is_teacher=False, base__lesson__teacher_id=teacher.id,
                                   field_of_study__lesson__teacher_id=teacher.id).distinct()
    if request.GET.get('table_search'):
        search = request.GET.get('table_search')
        students = students.filter(
            Q(first_name__contains=search) | Q(last_name__contains=search) | Q(email__contains=search))
    context = {
        'students': students
    }
    return JsonResponse({
        'body': render_to_string('management_panel_module/students_list_content.html', context)
    })


def management_header_references(request):
    return render(request, 'management_panel_module/components/management_header_references.html')


def management_footer_references(request):
    return render(request, 'management_panel_module/components/management_footer_references.html')


def management_sidebar(request):
    return render(request, 'management_panel_module/components/sidebar.html')


def management_navbar(request: HttpRequest):
    notifications = None
    if request.user.is_authenticated:
        user: User = request.user
        if user.is_teacher:
            custom_notifications = CustomNotification.objects.filter(from_teacher_id=user.id)
        elif not user.is_teacher or not user.is_superuser:
            notifications = Notification.objects.filter(user__in=[user])
            custom_notifications = CustomNotification.objects.filter(field_of_study_id=user.field_of_study.id,
                                                                     base_id=user.base.id)
        context = {'notifications': notifications, 'custom_notifications': custom_notifications}
    else:
        context = {}
    return render(request, 'management_panel_module/components/navbar.html', context)


class InfoAdminView(View):
    def get(self, request: HttpRequest):
        student_count = User.objects.filter(is_teacher=False, is_superuser=False, is_staff=False).count()
        teacher_count = User.objects.filter(is_teacher=True).count()
        lesson_count = Lesson.objects.all().count()
        set_home_work_count = SetHomeWork.objects.all().count()
        user_activity_objects = OnlineUserActivity.get_user_activities(timedelta(minutes=2))
        users = [user for user in user_activity_objects]
        context = {
            'student_count': student_count,
            'teacher_count': teacher_count,
            'lesson_count': lesson_count,
            'set_home_work_count': set_home_work_count,
            'number_of_active_users': len(users),
            'online_users': users[:8],
        }
        return render(request, 'adminlte/info_page.html', context)


class MyAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        student_count = User.objects.filter(is_teacher=False, is_superuser=False, is_staff=False).count()
        teacher_count = User.objects.filter(is_teacher=True).count()
        lesson_count = Lesson.objects.all().count()
        set_home_work_count = SetHomeWork.objects.all().count()
        user_activity_objects = OnlineUserActivity.get_user_activities(timedelta(minutes=2))
        users = [user for user in user_activity_objects]
        context = {
            'student_count': student_count,
            'teacher_count': teacher_count,
            'lesson_count': lesson_count,
            'set_home_work_count': set_home_work_count,
            'number_of_active_users': len(users),
            'online_users': users[:8],
        }
        return render(request, 'adminlte/info_page.html', context)
