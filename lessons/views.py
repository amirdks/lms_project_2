from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpRequest, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
# Create your views here.
from django.views import View
from django.views.generic import ListView, DeleteView

from account_module.models import User
from lesson_module.models import Lesson, SetHomeWork, HomeWorks
from management_panel_module.forms import SetHomeWorkForm, EditHomeWorkForm
from management_panel_module.mixins import JustTeacherMixin
from notification_module.models import Notification
from utils.time import end_time_calculator
from . import models
from .forms import SendHomeWorkForm
from .mixins import JustStudentOfLesson
from .models import FieldOfStudy, Base


# class HomeWorkView(LoginRequiredMixin, View):
#     login_url = reverse_lazy('login_page')
#
#     def get(self, request: HttpRequest, slug):
#         user: User = User.objects.filter(id=request.user.id).first()
#         if user.is_teacher is False:
#             field_of_study = FieldOfStudy.objects.filter(id=user.field_of_study.id).first()
#             base = models.Base.objects.filter(base_number=user.base.base_number).first()
#             lesson = Lesson.objects.filter(is_active=True, base_id=base.id,
#                                            field_of_study_id=field_of_study.id, slug__iexact=slug).first()
#             if lesson is None:
#                 raise Http404("درس مورد نطر یافت نشد")
#         elif user.is_teacher is True:
#             lesson = Lesson.objects.filter(is_active=True, slug__iexact=slug, teacher=user).first()
#             if lesson is None:
#                 raise Http404("درس مورد نطر یافت نشد")
#
#         home_work = SetHomeWork.objects.filter(lesson_id=lesson.id).first()
#         if home_work:
#             is_finished = end_time_calculator(home_work.end_at)
#             if is_finished is True and home_work.is_finished is False:
#                 home_work.is_finished = True
#                 home_work.save()
#             if home_work.is_finished and not user.is_teacher:
#                 home_work = None
#
#         if home_work:
#             if not user.is_teacher:
#                 home_works = HomeWorks.objects.filter(home_work_id=home_work.id, user_id=user.id).first()
#             elif user.is_teacher:
#                 home_works = HomeWorks.objects.filter(home_work_id=home_work.id).all()
#         else:
#             home_works = None
#
#         form = SendHomeWorkForm()
#         context = {
#             'lesson': lesson,
#             'home_work': home_work,
#             'form': form,
#             'home_works': home_works,
#         }
#         return render(request, 'lessons/home_work.html', context)
#
#     def post(self, request: HttpRequest, slug):
#         user: User = User.objects.filter(id=request.user.id).first()
#         field_of_study = FieldOfStudy.objects.filter(id=user.field_of_study.id).first()
#         base = models.Base.objects.filter(base_number=user.base.base_number).first()
#         lesson = Lesson.objects.filter(is_active=True, base_id=base.id,
#                                        field_of_study_id=field_of_study.id, slug__iexact=slug).first()
#         home_work = SetHomeWork.objects.filter(lesson_id=lesson.id).first()
#         form = SendHomeWorkForm(request.POST, request.FILES)
#         if form.is_valid():
#             new_home_work = HomeWorks(is_delivered=True, file=request.FILES['file'], home_work_id=home_work.id,
#                                       user_id=user.id)
#             new_home_work.save()
#             return HttpResponseRedirect(reverse('lessons_list_page'))
#
#         else:
#             form = SendHomeWorkForm()
#
#         return render(request, 'lessons/home_work.html', {'form': form, 'lesson': lesson})


# class LessonsList(LoginRequiredMixin, View):
#     login_url = reverse_lazy('login_page')
#
#     def get(self, request:HttpRequest):
#         user: User = User.objects.filter(id=request.user.id).first()
#         field_of_study = FieldOfStudy.objects.filter(id=user.field_of_study.id).first()
#         base = models.Base.objects.filter(base_number=user.base.base_number).first()
#         lessons = models.Lessons.objects.filter(is_active=True, base_id=base.id, field_of_study_id=field_of_study.id)
#         context = {
#             'lessons': lessons
#         }
#         return render(request, 'lessons/lessons_list.html', context)


class LessonsList(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = 'lessons/lessons_list.html'
    context_object_name = 'lessons'
    login_url = reverse_lazy('login_page')
    paginate_by = 6

    def get_queryset(self):
        query = super(LessonsList, self).get_queryset()
        user: User = User.objects.filter(id=self.request.user.id).first()
        if user.is_teacher is False:
            field_of_study = FieldOfStudy.objects.filter(id=user.field_of_study.id).first()
            base = models.Base.objects.filter(base_number=user.base.base_number).first()
            query = query.filter(is_active=True, base_id=base.id, field_of_study_id=field_of_study.id)
            if self.request.GET.get('table_search'):
                search = self.request.GET.get('table_search')
                query = query.filter(Q(title__contains=search))
        elif user.is_teacher is True:
            query = query.filter(is_active=True, teacher=user)
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
                else:
                    darsad = home_works.count() * 100 / set_home_work.count()
                    if home_works:
                        percent[lesson.title] = int(darsad)
            context['percent_of_sent_homework'] = percent
        return context


class ListSentHomeWorks(LoginRequiredMixin, JustTeacherMixin, View):
    login_url = reverse_lazy('login_page')

    def get(self, request: HttpRequest, id, pk):
        user: User = User.objects.filter(id=request.user.id).first()
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
            'home_work': home_work,
            'home_works': home_works,
        }
        return render(request, 'management_panel_module/sent_home_works.html', context)

    def post(self, request):
        pass


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
        context = {
            'home_works': home_works,
            'lesson': lesson,
            'send_home_works': send_home_works,
        }
        return render(request, 'lessons/home_work_list.html', context=context)


class HomeWorkView(LoginRequiredMixin, JustStudentOfLesson, View):
    login_url = reverse_lazy('login_page')

    def get(self, request, id, pk):
        form = SendHomeWorkForm()
        lesson = Lesson.objects.filter(id=id, is_active=True).first()
        home_work = SetHomeWork.objects.filter(id=pk).first()
        if lesson is None or home_work is None:
            raise Http404('درس و یا تکلیف مورد نظر یافت نشد')
        home_works = HomeWorks.objects.filter(home_work_id=home_work.id, user_id=request.user.id).first()
        context = {
            'home_work': home_work,
            'lesson': lesson,
            'form': form,
            'home_works': home_works
        }
        return render(request, 'lessons/home_work_page.html', context)

    def post(self, request, id, pk):
        form = SendHomeWorkForm(request.POST, request.FILES)
        user: User = request.user
        lesson = Lesson.objects.filter(is_active=True, id=id).first()
        home_work = SetHomeWork.objects.filter(id=pk).first()
        home_works = HomeWorks.objects.filter(home_work_id=home_work.id, user_id=user.id).first()
        if form.is_valid():
            file = form.files
            new_home_work = HomeWorks(user_id=user.id, file=request.FILES['file'], home_work_id=home_work.id,
                                      is_delivered=True)
            new_home_work.save()
            messages.success(request, 'تکلیف شما با موفقیت ارسال شد')
            return redirect(reverse('home_work_page', kwargs={'id': lesson.id, 'pk': home_work.id}))
        else:
            form = SendHomeWorkForm()
        return render(request, 'lessons/home_work_page.html',
                      {'home_works': home_works, 'form': form, 'home_work': home_work, 'lesson': lesson})


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
        set_home_work = HomeWorks.objects.filter(user_id=request.user.id, home_work_id=pk).first()
        set_home_work.delete()
        return redirect(reverse('home_work_page', kwargs={'id': id, 'pk': pk}))

    def post(self, request, id, pk):
        pass


class SetHomeWorkView(LoginRequiredMixin, JustTeacherMixin, View):
    login_url = reverse_lazy('login_page')

    def get(self, request: HttpRequest, lesson):
        lesson = lesson
        form = SetHomeWorkForm(initial={'lesson': lesson})
        context = {
            'form': form,
            'lessons': Lesson.objects.filter(teacher_id=request.user.id),
            'lesson': lesson
        }
        return render(request, 'management_panel_module/set_homework_page.html', context)

    def post(self, request: HttpRequest, lesson):
        form = SetHomeWorkForm(request.POST, initial={'lesson': lesson})
        lesson: Lesson = lesson
        if form.is_valid():
            teacher_id = request.user.id
            title = form.cleaned_data.get('title')
            ends_at = form.cleaned_data.get('end_at')
            is_finished = end_time_calculator(ends_at)
            if is_finished:
                messages.error(request, 'لطفا به زمان پایان دقت کنید')
            else:
                lesson = form.cleaned_data.get('lesson')
                description = form.cleaned_data.get('description')
                new_home_work = SetHomeWork(title=title, end_at=ends_at, lesson_id=lesson.id, description=description,
                                            teacher_id=teacher_id)
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
        form = SetHomeWorkForm(initial={'lesson': lesson})
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
