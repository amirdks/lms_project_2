from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, Http404
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView

from account_module.models import User
from lesson_module.models import Lesson, SetHomeWork
from lessons import models
from lessons.models import FieldOfStudy


class HomeWorkView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_page')

    def get(self, request: HttpRequest, slug):
        user: User = User.objects.filter(id=request.user.id).first()
        if user.is_teacher is False:
            field_of_study = FieldOfStudy.objects.filter(id=user.field_of_study.id).first()
            base = models.Base.objects.filter(base_number=user.base.base_number).first()
            lesson = Lesson.objects.filter(is_active=True, base_id=base.id,
                                           field_of_study_id=field_of_study.id, slug__iexact=slug).first()
            if lesson is None:
                raise Http404("درس مورد نطر یافت نشد")
        elif user.is_teacher is True:
            lesson = Lesson.objects.filter(is_active=True, slug__iexact=slug, teacher=user).first()
            if lesson is None:
                raise Http404("درس مورد نطر یافت نشد")
        context = {
            'lesson': lesson
        }
        return render(request, 'lessons/home_work.html', context)


class HomeWorkList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login_page')
    model = SetHomeWork
    template_name = 'home_work_module/home_works_list.html'

    def get_queryset(self):
        query = super(HomeWorkList, self).get_queryset()
        query = query.filter()
