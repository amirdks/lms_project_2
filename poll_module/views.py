from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from management_panel_module.mixins import PermissionMixin
from poll_module.forms import CreatePollForm
from poll_module.models import Poll


# Create your views here.

class CreatePoll(LoginRequiredMixin, PermissionMixin, CreateView):
    permission_list = ['is_teacher', 'is_superuser', 'is_staff']
    form_class = CreatePollForm
    model = Poll
    success_url = reverse_lazy('lessons_list_page')
    template_name = 'poll_module/create_poll.html'
    context_object_name = 'form'

    def get_form_kwargs(self):
        context = super(CreatePoll, self).get_form_kwargs()
        context['user'] = self.request.user
        return context


class UpdatePoll(LoginRequiredMixin, PermissionMixin, UpdateView):
    model = Poll
    form_class = CreatePollForm
    template_name = 'poll_module/create_poll.html'
    context_object_name = 'poll'
    success_url = reverse_lazy('lessons_list_page')
    permission_list = ['is_teacher', 'is_superuser', 'is_staff']

    def get_form_kwargs(self):
        context = super(UpdatePoll, self).get_form_kwargs()
        context['user'] = self.request.user
        return context
