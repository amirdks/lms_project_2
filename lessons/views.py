import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Avg, Count
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
# Create your views here.
from django.views import View
from django.views.generic import ListView

from account_module.models import User
from lesson_module.models import Lesson, SetHomeWork, HomeWorks, HomeWorkFiles, PoodemanAndNobat
from management_panel_module.forms import SetHomeWorkForm, EditHomeWorkForm
from management_panel_module.mixins import JustTeacherMixin
from notification_module.models import Notification
from utils.time import end_time_calculator
from .forms import SendHomeWorkForm
from .mixins import JustStudentOfLesson


class LessonsList(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = 'lessons/lessons_list.html'
    context_object_name = 'lessons'
    login_url = reverse_lazy('login_page')
    paginate_by = 6
    ordering = 'title'

    def get_queryset(self):
        query: Lesson.objects = super(LessonsList, self).get_queryset()
        user: User = User.objects.filter(id=self.request.user.id).first()
        if user.is_teacher is False:
            query = query.filter(is_active=True, base_id=user.base.id, field_of_study_id=user.field_of_study.id)
        elif user.is_teacher is True:
            query = query.filter(is_active=True, teacher_id=user.id)
        if self.request.GET.get('table_search'):
            search = self.request.GET.get('table_search')
            query = query.filter(
                Q(title__contains=search) | Q(field_of_study__title__contains=search) | Q(
                    base__title__contains=search))
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
            context['percent_of_sent_homework'] = percent
        return context


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
        home_work = SetHomeWork.objects.filter(id=pk).first()
        lesson = Lesson.objects.filter(id=id).first()
        home_works = HomeWorks.objects.filter(home_work_id=home_work.id).all()
        for sent_home_work in home_works:
            score_user = request.POST.get(str(sent_home_work.user.id))
            if score_user:
                if float(score_user) <= sent_home_work.home_work.score_weight:
                    sent_home_work.score = float(score_user)
                    sent_home_work.score_percent = sent_home_work.score_percent_func()
                    sent_home_work.save()
                else:
                    messages.error(request, 'لطفا به وزن نمرات دقت کنید')
        context = {
            'lesson': lesson,
            'set_home_work': home_work,
            'home_works': home_works,
        }
        return render(request, 'management_panel_module/sent_home_works.html', context)


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
            'poodemans':poodemans,
            'nobats': nobats,
        }
        return render(request, 'lessons/home_work_list.html', context=context)


class HomeWorkView(LoginRequiredMixin, JustStudentOfLesson, View):
    login_url = reverse_lazy('login_page')

    def get(self, request, id, pk):
        form = SendHomeWorkForm()
        lesson = Lesson.objects.filter(id=id, is_active=True).first()
        home_work = SetHomeWork.objects.filter(id=pk).first()
        allowed_formats = ','.join([format.get('format') for format in list(home_work.allowed_formats.values())])
        if lesson is None or home_work is None:
            raise Http404('درس و یا تکلیف مورد نظر یافت نشد')
        home_works = HomeWorks.objects.filter(home_work_id=home_work.id, user_id=request.user.id).first()
        context = {
            'home_work': home_work,
            'lesson': lesson,
            'form': form,
            'home_works': home_works,
            'allowed_formats': allowed_formats,
        }
        return render(request, 'lessons/home_work_page.html', context)

    def post(self, request, id, pk):
        form = SendHomeWorkForm(request.POST, request.FILES)
        user: User = request.user
        lesson = Lesson.objects.filter(is_active=True, id=id).first()
        home_work = SetHomeWork.objects.filter(id=pk).first()
        home_works = HomeWorks.objects.filter(home_work_id=home_work.id, user_id=user.id).first()
        allowed_formats = ','.join([format.get('format') for format in list(home_work.allowed_formats.values())])
        if form.is_valid():
            if not home_works:
                message = form.cleaned_data.get('message')
                new_home_work = HomeWorks(user_id=user.id, home_work_id=home_work.id,
                                          is_delivered=True, message=message)
                new_home_work.save()
            for f in request.FILES.getlist('file'):
                value = round(f.size / 1000000, 2)
                if not os.path.splitext(f.__str__())[-1].lower() in allowed_formats:
                    messages.error(request, 'نمیتونی فایل {} رو بفرسیتی'.format(f.__str__()))
                elif value > home_work.max_size:
                    form.add_error('file', 'حجم فایل ارسال شده بالاتر از حد مجاز است')
                else:
                    if home_works:
                        new_file = HomeWorkFiles.objects.create(home_work_id=home_works.id, file=f)
                    else:
                        new_file = HomeWorkFiles.objects.create(home_work_id=new_home_work.id, file=f)
                    new_file.save()
                    messages.success(request, 'تکلیف شما با موفقیت ارسال شد')
            return redirect(reverse('home_work_page', kwargs={'id': lesson.id, 'pk': home_work.id}))
        else:
            form = SendHomeWorkForm()
        context = {'home_works': home_works, 'form': form, 'home_work': home_work, 'lesson': lesson,
                   'allowed_formats': allowed_formats}
        return render(request, 'lessons/home_work_page.html', context)


class DeleteHomeWorkView(LoginRequiredMixin, JustTeacherMixin, View):
    login_url = reverse_lazy('login_page')

    def get(self, request, id, pk):
        lesson = Lesson.objects.filter(id=id).first()
        home_work = SetHomeWork.objects.filter(id=pk).first()
        home_work.delete()
        messages.add_message(request, messages.SUCCESS, 'تکلیف مورد نطر با موفقیت حذف شد')
        return redirect(reverse('list_home_works', kwargs={'id': lesson.id}))

    def post(self, request, id, pk):
        pass


class DeleteSentHomeWorkView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_page')

    def get(self, request, id, pk):
        file = HomeWorkFiles.objects.filter(id=pk).first()
        pk = file.home_work.home_work.id
        file.delete()
        return redirect(reverse('home_work_page', kwargs={'id': id, 'pk': pk}))

    def post(self, request, id, pk):
        pass


class SetHomeWorkView(LoginRequiredMixin, JustTeacherMixin, View):
    login_url = reverse_lazy('login_page')

    def get(self, request: HttpRequest, lesson):
        lesson = Lesson.objects.filter(id=lesson).first()
        form = SetHomeWorkForm()
        if lesson.poodeman_or_nobat == 'poodeman':
            form.fields['poodeman_or_nobat'].queryset = PoodemanAndNobat.objects.filter(type__iexact='poodeman')
        else:
            form.fields['poodeman_or_nobat'].queryset = PoodemanAndNobat.objects.filter(type__iexact='nobat')
        context = {
            'form': form,
            'lessons': Lesson.objects.filter(teacher_id=request.user.id),
            'lesson': lesson
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
            is_finished = end_time_calculator(ends_at)
            if is_finished:
                messages.error(request, 'لطفا به زمان پایان دقت کنید')
            else:
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
                                                               home_work_id=new_home_work.id, text=notification_text)
                new_notification.user.set(notification_users)
                new_notification.save()
                messages.add_message(request, messages.SUCCESS, 'تکلیف جدید با موفقیت قرار گرفت')
                if lesson:
                    return redirect(reverse('list_home_works', kwargs={'id': lesson.id}))
                else:
                    return redirect(reverse('management_panel_page'))
        form = SetHomeWorkForm()
        if lesson.poodeman_or_nobat == 'poodeman':
            form.fields['poodeman_or_nobat'].queryset = PoodemanAndNobat.objects.filter(type__iexact='poodeman')
        else:
            form.fields['poodeman_or_nobat'].queryset = PoodemanAndNobat.objects.filter(type__iexact='nobat')
        contex = {
            'form': form,
            'lesson': lesson,
        }
        return render(request, 'management_panel_module/set_homework_page.html', contex)


class EditHomeWorkView(View):
    def get(self, request: HttpRequest, id, pk):
        lesson: Lesson = Lesson.objects.filter(id=id).first()
        home_work = SetHomeWork.objects.filter(id=pk).first()
        form = EditHomeWorkForm(instance=home_work)
        context = {
            'form': form,
            'lesson': lesson,
            'home_work': home_work,
        }
        return render(request, 'lessons/edit_home_work.html', context)

    def post(self, request: HttpRequest, id, pk):
        lesson: Lesson = Lesson.objects.filter(id=id).first()
        home_work = SetHomeWork.objects.filter(id=pk).first()
        form = EditHomeWorkForm(request.POST, instance=home_work)
        if form.is_valid():
            form.save(commit=True)
            messages.add_message(request, messages.SUCCESS, 'تکلیف با موفقیت ویرایش شد')
            return redirect(reverse('list_home_works', kwargs={'id': id}))
        form = EditHomeWorkForm()
        context = {
            'form': form,
            'lesson': lesson,
            'home_work': home_work,
        }
        return render(request, 'lessons/edit_home_work.html', context)


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
        set_home_works = SetHomeWork.objects.filter(lesson_id=lesson.id, poodeman_or_nobat_id=pood_or_nobat.id).all()
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
        set_home_works = SetHomeWork.objects.filter(lesson_id=id, poodeman_or_nobat__slug__exact=slug,
                                                    teacher_id=request.user.id)
        sent_home_works = HomeWorks.objects.filter(home_work__lesson_id=id, home_work__teacher_id=request.user.id,
                                                   home_work__poodeman_or_nobat__slug=slug,
                                                   user_id=user_id)
        for sent_home_work in sent_home_works:
            score_user = request.POST.get(str(sent_home_work.id))
            if score_user:
                if float(score_user) <= sent_home_work.home_work.score_weight:
                    sent_home_work.score = float(score_user)
                    sent_home_work.score_percent = sent_home_work.score_percent_func()
                    sent_home_work.save()
                else:
                    messages.error(request, 'لطفا به وزن نمرات دقت کنید')
        context = {
            'sent_home_works': sent_home_works,
            'set_home_works': set_home_works,
            'leeson_id': id,
            'set_home_work': set_home_works.first(),
            'user_id': user_id
        }
        return render(request, 'lessons/student_list_sent_homeworks.html', context)
