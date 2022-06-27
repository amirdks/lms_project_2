from datetime import timedelta

from django.contrib import messages
from django.contrib.admin import AdminSite
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from online_users.models import OnlineUserActivity

from account_module.models import User
from lesson_module.models import Lesson, SetHomeWork
from management_panel_module.forms import SetHomeWorkForm
from management_panel_module.mixins import JustTeacherMixin
from notification_module.models import Notification
from utils.time import end_time_calculator


class ManagementPanelView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login_page')
    template_name = 'management_panel_module/base.html'


class StudentsListView(LoginRequiredMixin, JustTeacherMixin, View):
    login_url = reverse_lazy('login_page')

    def get(self, request: HttpRequest):
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

        return render(request, 'management_panel_module/students_list.html', context)


class SetHomeWorkView(LoginRequiredMixin, JustTeacherMixin, View):

    def get(self, request: HttpRequest):
        form = SetHomeWorkForm()
        context = {
            'form': form,
            'lessons': Lesson.objects.filter(teacher_id=request.user.id)
        }
        return render(request, 'management_panel_module/set_homework_page.html', context)

    def post(self, request: HttpRequest):
        form = SetHomeWorkForm(request.POST)
        if form.is_valid():
            teacher_id = request.user.id
            title = form.cleaned_data.get('title')
            ends_at = form.cleaned_data.get('end_at')
            allowed_formats = form.cleaned_data.get('format')
            max_size = form.cleaned_data.get('max_size')
            is_finished = end_time_calculator(ends_at)
            if is_finished:
                messages.error(request, 'لطفا به زمان پایان دقت کنید')
            else:
                lesson = form.cleaned_data.get('lesson')
                description = form.cleaned_data.get('description')
                new_home_work = SetHomeWork.objects.create(title=title, end_at=ends_at, lesson_id=lesson.id, description=description,
                                            teacher_id=teacher_id, max_size=max_size)
                new_home_work.allowed_formats.set(allowed_formats)
                new_home_work.save()
                notification_users = User.objects.filter(field_of_study_id=lesson.field_of_study.id,
                                                         base_id=lesson.base.id,
                                                         is_teacher=False)
                notification_text = f'یک تکلیف جدید مربوط به درس {lesson.title} به نام {new_home_work.title} قرار گرفت'
                new_notification = Notification.objects.create(from_user_id=request.user.id,
                                                               home_work_id=new_home_work.id, text=notification_text)
                new_notification.user.set(notification_users)
                new_notification.save()
                return redirect(reverse('management_panel_page'))

        form = SetHomeWorkForm()
        contex = {
            'form': form
        }
        return render(request, 'management_panel_module/set_homework_page.html', contex)


def management_header_references(request):
    return render(request, 'management_panel_module/components/management_header_references.html')


def management_footer_references(request):
    return render(request, 'management_panel_module/components/management_footer_references.html')


def management_sidebar(request):
    return render(request, 'management_panel_module/components/sidebar.html')


def management_navbar(request):
    if request.user.is_authenticated:
        user: User = request.user
        notifications = Notification.objects.filter(user__in=[user])
        context = {'notifications': notifications}
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
    @never_cache
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
