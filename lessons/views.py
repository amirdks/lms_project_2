import json
import os
import time
from datetime import datetime, timedelta

import jalali_date
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.db.models import Q, Avg, Count
from django.http import HttpRequest, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
# Create your views here.
from django.views import View
from django.views.generic import ListView

from account_module.models import User
from lesson_module.models import Lesson, SetHomeWork, HomeWorks, HomeWorkFiles, PoodemanAndNobat
from management_panel_module.filters import StudentListResultFilter
from management_panel_module.forms import SetHomeWorkForm, EditHomeWorkForm
from management_panel_module.mixins import JustTeacherMixin
from notification_module.models import Notification
from utils.time import end_time_calculator
from .filters import LessonListResultFilter
from .forms import SendHomeWorkForm
from .mixins import JustStudentOfLesson
from .serializer import LessonSerializer


class LessonsList(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = 'lessons/lessons_list.html'
    context_object_name = 'lessons'
    login_url = reverse_lazy('login_page')
    paginate_by = 6
    ordering = 'title'

    def post(self, request):
        lessons = self.get_queryset()
        lessons_json=[]
        if self.request.POST.get('table_search'):
            search = self.request.POST.get('table_search')
            lessons = lessons.filter(
                Q(title__contains=search) | Q(field_of_study__title__contains=search) | Q(
                    base__title__contains=search))
            lessons_json = LessonSerializer(lessons, many=True).data
            # print(lessons_json)
        return JsonResponse({'body': render_to_string('lessons/includes/lessons_list_content.html',
                                                      context={'lessons': lessons,
                                                               'percent_of_sent_homework': 0}),
                             'lessons_json': lessons_json})

    def get_queryset(self):
        query: Lesson.objects = super(LessonsList, self).get_queryset()
        user: User = User.objects.filter(id=self.request.user.id).first()
        if user.is_teacher is False:
            query = query.filter(is_active=True, base_id=user.base.id, field_of_study_id=user.field_of_study.id)
        elif user.is_teacher is True:
            query = query.filter(is_active=True, teacher_id=user.id)
            # if self.request.GET.get('base') or self.request.GET.get('field_of_study'):
            query = LessonListResultFilter(self.request.GET, queryset=query).qs
        return query

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LessonsList, self).get_context_data(**kwargs)
        user: User = self.request.user
        if not user.is_teacher:
            lessons = Lesson.objects.filter(field_of_study_id=user.field_of_study.id, base_id=user.base.id,
                                            is_active=True).all()
            percent = {}
            for lesson in lessons:
                set_home_work = SetHomeWork.objects.filter(lesson_id=lesson.id)
                home_works = HomeWorks.objects.filter(user_id=user.id, home_work__lesson_id=lesson.id).all()
                if set_home_work.count() == 0 or home_works.count() == 0:
                    darsad = 0
                    percent[lesson.title] = int(darsad)
                else:
                    darsad = home_works.count() * 100 / set_home_work.count()
                    if home_works:
                        percent[lesson.title] = int(darsad)
            percent = percent
            context['percent_of_sent_homework'] = percent
        context['filter'] = StudentListResultFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ListHomeWorks(LoginRequiredMixin, JustStudentOfLesson, View):
    login_url = reverse_lazy('login_page')

    def get(self, request: HttpRequest, id):
        user: User = request.user
        lesson = Lesson.objects.filter(id=id).first()
        if lesson is None:
            raise Http404('درس مورد نطر یافت نشد')
        if user.is_teacher:
            home_works = SetHomeWork.objects.filter(lesson__is_active=True, lesson_id=id, teacher_id=user.id).order_by(
                '-start_at')
        else:
            home_works = SetHomeWork.objects.filter(lesson_id=id, lesson__is_active=True,
                                                    lesson__base_id=user.base.id,
                                                    lesson__field_of_study_id=user.field_of_study.id).order_by(
                '-start_at')
        if home_works:
            for home_work in home_works:
                is_finished = end_time_calculator(home_work.end_at)
                if is_finished is True and home_work.is_finished is False:
                    home_work.is_finished = True
                    home_work.save()
        send_home_works = HomeWorks.objects.filter(home_work__lesson_id=lesson.id, user_id=user.id)
        poodemans = PoodemanAndNobat.objects.filter(type__iexact='poodeman')
        nobats = PoodemanAndNobat.objects.filter(type__iexact='nobat')
        context = {
            'home_works': home_works,
            'lesson': lesson,
            'send_home_works': send_home_works,
            'poodemans': poodemans,
            'nobats': nobats,
        }
        return render(request, 'lessons/home_work_list.html', context=context)


class HomeWorkView(LoginRequiredMixin, JustStudentOfLesson, View):
    login_url = reverse_lazy('login_page')

    def setup(self, request, *args, **kwargs):
        id = kwargs.get('id')
        pk = kwargs.get('pk')
        self.context = {}
        self.context['home_work'] = get_object_or_404(SetHomeWork, id=pk)
        self.context['form'] = SendHomeWorkForm()
        self.context['lesson'] = Lesson.objects.filter(id=id, is_active=True).first()
        self.context['home_works'] = HomeWorks.objects.filter(home_work_id=self.context.get('home_work').id,
                                                              user_id=request.user.id).first()
        self.context['allowed_formats'] = ','.join(
            [format.get('format') for format in list(self.context.get('home_work').allowed_formats.values())])
        return super(HomeWorkView, self).setup(request, *args, **kwargs)

    def get(self, request, id, pk):
        if self.context.get('lesson') is None or self.context.get('home_work') is None:
            raise Http404('درس و یا تکلیف مورد نظر یافت نشد')
        return render(request, 'lessons/home_work_page.html', self.context)

    def post(self, request: HttpRequest, id, pk):
        user: User = request.user
        lesson = self.context.get('lesson')
        home_work = self.context.get('home_work')
        home_works = HomeWorks.objects.filter(home_work_id=self.context.get('home_work').id,
                                              user_id=request.user.id).first()
        allowed_formats = self.context.get('allowed_formats')
        form = SendHomeWorkForm(home_work, allowed_formats, request.POST, request.FILES)
        is_first_time = False
        if form.is_valid():
            f = request.FILES.get('file')
            if home_works:
                new_file = HomeWorkFiles.objects.create(home_work_id=home_works.id, file=f)
            else:
                message = form.cleaned_data.get('message')
                home_works = HomeWorks(
                    user_id=user.id, home_work_id=home_work.id,
                    is_delivered=True, message=message
                )
                home_works.save()
                new_file = HomeWorkFiles.objects.create(home_work_id=home_works.id, file=f)
                is_first_time = True
            new_file.save()
            home_works = HomeWorks.objects.filter(
                home_work_id=self.context.get('home_work').id,
                user_id=request.user.id
            ).first()
            sent_homeworks_component = render_to_string('lessons/includes/sent_homeworks_list_component.html',
                                                        context={'home_works': home_works, 'lesson': lesson})
            return JsonResponse(
                {'status': 'success', 'body': sent_homeworks_component, 'is_first_time': is_first_time,
                 'message': 'آپلود فایل موفقیت آمیز بود'})
        if form.errors:
            for field in form:
                for error in field.errors:
                    error = error
        return JsonResponse({
            'status': 'failed',
            'error': error
        })


class DeleteHomeWorkView(LoginRequiredMixin, JustTeacherMixin, View):
    login_url = reverse_lazy('login_page')

    def post(self, request, id, pk):
        time.sleep(3)
        try:
            lesson = Lesson.objects.get(id=id)
            home_work = SetHomeWork.objects.get(id=pk)
        except (SetHomeWork.DoesNotExist, Lesson.DoesNotExist) as e:
            return JsonResponse({'status': 'danger', 'persian_status': 'شکست', 'message': 'تکلیف پیدا نشد'})
        home_work.delete()
        home_works = SetHomeWork.objects.filter(lesson_id=id)
        send_home_works = HomeWorks.objects.filter(home_work__lesson_id=lesson.id, user_id=request.user.id)
        home_works_list = render_to_string('lessons/includes/home_works_list_component.html',
                                           context={'request': request, 'lesson': lesson,
                                                    'send_home_works': send_home_works, 'home_works': home_works})
        return JsonResponse(
            {'body': home_works_list, 'status': 'success', 'persian_status': 'موفق',
             'message': 'تکلیف مورد نطر با موفقیت حذف شد'})

    def get(self, request, id, pk):
        try:
            lesson = Lesson.objects.get(id=id)
            home_work = SetHomeWork.objects.get(id=pk)
        except (SetHomeWork.DoesNotExist, Lesson.DoesNotExist) as e:
            raise Http404('تکلیف مورد نطر پیدا نشد')
        home_work.delete()
        return redirect(reverse('list_home_works', kwargs={'id': lesson.id}))


class DeleteSentHomeWorkView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_page')

    def post(self, request, id, pk, file_id):
        time.sleep(3)
        file = HomeWorkFiles.objects.filter(id=file_id).first()
        file.delete()
        lesson = Lesson.objects.filter(id=id, is_active=True).first()
        home_works = HomeWorks.objects.filter(home_work_id=pk,
                                              user_id=request.user.id).first()
        sent_homeworks_component = render_to_string('lessons/includes/sent_homeworks_list_component.html',
                                                    context={'home_works': home_works, 'lesson': lesson})
        return JsonResponse({'status': 'success', 'body': sent_homeworks_component})


class SetHomeWorkView(LoginRequiredMixin, JustTeacherMixin, View):
    login_url = reverse_lazy('login_page')

    def get(self, request: HttpRequest, lesson):
        lesson = Lesson.objects.filter(id=lesson).first()
        jdate = jalali_date.date2jalali(datetime.now()).strftime('%m/%d/%Y')
        form = SetHomeWorkForm()
        if lesson.poodeman_or_nobat == 'poodeman':
            form.fields['poodeman_or_nobat'].queryset = PoodemanAndNobat.objects.filter(type__iexact='poodeman')
        else:
            form.fields['poodeman_or_nobat'].queryset = PoodemanAndNobat.objects.filter(type__iexact='nobat')
        context = {
            'form': form,
            'lessons': Lesson.objects.filter(teacher_id=request.user.id),
            'lesson': lesson,
            'date': jdate
        }
        return render(request, 'management_panel_module/set_homework_page.html', context)

    def post(self, request: HttpRequest, lesson):
        form = SetHomeWorkForm(request.POST)
        lesson = Lesson.objects.filter(id=lesson).first()
        if form.is_valid():
            teacher_id = request.user.id
            title = form.cleaned_data.get('title')
            ends_at = form.cleaned_data.get('end_at')
            allowed_formats = form.cleaned_data.get('format')
            max_size = form.cleaned_data.get('max_size')
            poodeman_or_nobat = form.cleaned_data.get('poodeman_or_nobat')
            score_weight = form.cleaned_data.get('score_weight')
            description = form.cleaned_data.get('description')
            new_home_work = SetHomeWork.objects.create(title=title, end_at=ends_at, lesson_id=lesson.id,
                                                       description=description,
                                                       teacher_id=teacher_id, max_size=max_size,
                                                       poodeman_or_nobat_id=poodeman_or_nobat.id,
                                                       score_weight=score_weight)
            new_home_work.allowed_formats.set(allowed_formats)
            new_home_work.save()
            notification_users = User.objects.filter(field_of_study_id=lesson.field_of_study.id,
                                                     base_id=lesson.base.id,
                                                     is_teacher=False)
            notification_text = f'یک تکلیف جدید مربوط به درس {lesson.title} به نام {new_home_work.title} قرار گرفت'
            new_notification = Notification.objects.create(from_user_id=request.user.id,
                                                           home_work_id=new_home_work.id,
                                                           text=notification_text)
            new_notification.user.set(notification_users)
            new_notification.save()
            time.sleep(3)
            return JsonResponse(
                {'redirect': reverse('list_home_works', kwargs={'id': lesson.id}), 'status': 'success',
                 'message': 'تکلیف جدید با موفقیت قرار گرفت درحال تغییر مسیر ...'})
        if form.errors:
            for field in form:
                for error in field.errors:
                    error = error
                    field_name = field.label
        return JsonResponse({'status': 'failed', 'field_name': field_name, 'message': error})


class EditHomeWorkView(View):
    def get(self, request: HttpRequest, id, pk):
        lesson: Lesson = Lesson.objects.filter(id=id).first()
        home_work = SetHomeWork.objects.filter(id=pk).first()
        form = EditHomeWorkForm(instance=home_work)
        jdate = jalali_date.date2jalali(datetime.now()).strftime('%m/%d/%Y')
        if lesson.poodeman_or_nobat == 'poodeman':
            form.fields['poodeman_or_nobat'].queryset = PoodemanAndNobat.objects.filter(type__iexact='poodeman')
        else:
            form.fields['poodeman_or_nobat'].queryset = PoodemanAndNobat.objects.filter(type__iexact='nobat')
        context = {
            'form': form,
            'lesson': lesson,
            'home_work': home_work,
            'date': jdate,
        }
        return render(request, 'lessons/edit_home_work.html', context)

    def post(self, request: HttpRequest, id, pk):
        lesson: Lesson = Lesson.objects.filter(id=id).first()
        home_work = SetHomeWork.objects.filter(id=pk).first()
        form = EditHomeWorkForm(request.POST, instance=home_work)
        time.sleep(3)
        if form.is_valid():
            form.save(commit=True)
            messages.add_message(request, messages.SUCCESS, 'تکلیف با موفقیت ویرایش شد')
            return JsonResponse(
                {'redirect': reverse('list_home_works', kwargs={'id': lesson.id}), 'status': 'success',
                 'message': 'تکلیف جدید با موفقیت قرار گرفت درحال تغییر مسیر ...'})
        error = ''
        field_name = ''
        if form.errors:
            for field in form:
                for error in field.errors:
                    error = error
                    field_name = field.label
        return JsonResponse({'status': 'failed', 'field_name': field_name, 'message': error})


class StudentListHomeWorks(JustTeacherMixin, LoginRequiredMixin, View):
    login_url = reverse_lazy('login_page')

    def get(self, request, id, slug):
        lesson = Lesson.objects.get(id=id)
        pood_or_nobat = PoodemanAndNobat.objects.get(slug__exact=slug)
        students = User.objects.filter(field_of_study_id=lesson.field_of_study.id, base_id=lesson.base.id).all()
        if request.GET.get('table_search'):
            search = request.GET.get('table_search')
            students = students.filter(
                Q(first_name__contains=search) | Q(last_name__contains=search) | Q(email__contains=search))
        set_home_works = SetHomeWork.objects.filter(lesson_id=lesson.id,
                                                    poodeman_or_nobat_id=pood_or_nobat.id).all()
        sent_home_works = HomeWorks.objects.filter(home_work_id__in=set_home_works).all()
        main_context = {}
        for student in students:
            student_sent_home_works = sent_home_works.filter(user_id=student.id).aggregate(
                percent_average=Avg('score_percent'), home_work_count=Count('home_work'))
            score_percent = student_sent_home_works.get('percent_average')
            sent_home_works_count = student_sent_home_works.get('home_work_count')
            set_home_work_count = set_home_works.count()
            if sent_home_works_count < set_home_work_count and score_percent:
                for x in range(set_home_work_count - sent_home_works_count):
                    score_percent_not_sent = score_percent * sent_home_works_count / (sent_home_works_count + 1)
            else:
                score_percent_not_sent = 0
                score_percent = 0
            main_context.update(
                {student.__str__(): {'user': student, 'score_percent': score_percent,
                                     'count': sent_home_works_count,
                                     'score_percent_not_sent': score_percent_not_sent}})
        context = {
            'students': students,
            'main': main_context,
            'set_home_work_count': set_home_work_count,
            'lesson': lesson,
            'set_home_work': set_home_works.first()
        }
        return render(request, 'lessons/students-list-homeworks.html', context)


class StudentLIstSentHomeWorks(JustTeacherMixin, LoginRequiredMixin, View):
    login_url = reverse_lazy('login_page')

    def get(self, request, id, slug, user_id):
        set_home_works = SetHomeWork.objects.filter(lesson_id=id, poodeman_or_nobat__slug__exact=slug,
                                                    teacher_id=request.user.id)
        sent_home_works = HomeWorks.objects.filter(home_work__lesson_id=id, home_work__teacher_id=request.user.id,
                                                   home_work__poodeman_or_nobat__slug=slug,
                                                   user_id=user_id)
        if request.GET.get('table_search'):
            search = request.GET.get('table_search')
            sent_home_works = sent_home_works.filter(Q(home_work__title__contains=search))
        context = {
            'sent_home_works': sent_home_works,
            'set_home_works': set_home_works,
            'leeson_id': id,
            'set_home_work': set_home_works.first(),
            'user_id': user_id
        }
        return render(request, 'lessons/student_list_sent_homeworks.html', context)

    def post(self, request, id, slug, user_id):
        sent_home_works = HomeWorks.objects.filter(home_work__lesson_id=id, home_work__teacher_id=request.user.id,
                                                   home_work__poodeman_or_nobat__slug=slug,
                                                   user_id=user_id)
        time.sleep(2)
        for sent_home_work in sent_home_works:
            score_user = json.loads(request.POST.get('score_form')).get(str(sent_home_work.id))
            if score_user:
                if float(score_user) <= sent_home_work.home_work.score_weight:
                    sent_home_work.score = float(score_user)
                    sent_home_work.score_percent = sent_home_work.score_percent_func()
                    sent_home_work.save()
                else:
                    return JsonResponse({'status': 'failed', 'id': sent_home_work.id, 'score': score_user})
        return JsonResponse({'status': 'success'})


class ListSentHomeWorks(LoginRequiredMixin, JustTeacherMixin, View):
    login_url = reverse_lazy('login_page')

    def get(self, request: HttpRequest, id, pk):
        home_work = SetHomeWork.objects.filter(id=pk).first()
        lesson = Lesson.objects.filter(id=id).first()
        if home_work is None:
            raise Http404("تکلیف مورد نطر یافت نشد")
        if home_work:
            home_works = HomeWorks.objects.filter(home_work_id=home_work.id).all()
        else:
            home_works = None

        if request.GET.get('table_search'):
            search = request.GET.get('table_search')
            home_works = home_works.filter(Q(user__username__contains=search) | Q(user__first_name__contains=search)
                                           | Q(user__last_name__contains=search))
        context = {
            'lesson': lesson,
            'set_home_work': home_work,
            'home_works': home_works,
        }
        return render(request, 'management_panel_module/sent_home_works.html', context)

    def post(self, request: HttpRequest, id, pk):
        time.sleep(3)
        home_work = SetHomeWork.objects.filter(id=pk).first()
        sent_home_works = HomeWorks.objects.filter(home_work_id=home_work.id).all()
        for sent_home_work in sent_home_works:
            score_user = json.loads(request.POST.get('score_form')).get(str(sent_home_work.id))
            if score_user:
                if float(score_user) <= sent_home_work.home_work.score_weight:
                    sent_home_work.score = float(score_user)
                    sent_home_work.score_percent = sent_home_work.score_percent_func()
                    sent_home_work.save()
                else:
                    return JsonResponse({'status': 'failed', 'id': sent_home_work.id, 'score': score_user})
        return JsonResponse({'status': 'success'})


def just_for_test(request):
    return render(request, 'lessons/date_picker_test.html')
