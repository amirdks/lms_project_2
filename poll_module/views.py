import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse, Http404, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from management_panel_module.mixins import PermissionMixin
from poll_module.forms import CreatePollForm, PollOptionForm
from poll_module.models import Poll, PollOptions
from utils.casual_functions import poll_render_to_string


# Create your views here.
class PollList(ListView):
    model = Poll
    template_name = 'poll_module/poll_list.html'
    context_object_name = 'polls'


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

    def get_context_data(self, **kwargs):
        context = super(UpdatePoll, self).get_context_data(**kwargs)
        poll = self.get_object()
        poll_options = PollOptions.objects.filter(poll_id=poll.id)
        context['poll_options'] = poll_options
        return context

    def get_form_kwargs(self):
        context = super(UpdatePoll, self).get_form_kwargs()
        context['user'] = self.request.user
        return context


class DeletePoll(LoginRequiredMixin, PermissionMixin, DeleteView):
    model = Poll
    success_url = reverse_lazy('lessons_list_page')
    permission_list = ['is_teacher', 'is_superuser', 'is_staff']


def add_poll_option(request: HttpRequest, pk):
    if request.method == 'POST':
        poll = get_object_or_404(Poll, pk=pk)
        form = PollOptionForm(request.POST, poll=poll)
        time.sleep(3)
        if form.is_valid():
            form.save()
            body = poll_render_to_string(pk)
            return JsonResponse({'status': 'success', 'body': body, 'message': 'گزینه با موفقیت قرار گرفت'})
        error = 'مشکلی وجود دارد'
        for field in form:
            if field.errors:
                for error in field.errors:
                    error = error
        return JsonResponse({'status': 'failed', 'message': error})
    raise Http404("page not found")


def delete_poll_option(request, pk, id):
    if request.method == 'POST':
        time.sleep(3)
        try:
            poll_option = PollOptions.objects.get(id=id)
            poll_option.delete()
            body = poll_render_to_string(pk)
            return JsonResponse({'status': 'success', 'body': body, 'message': 'گزینه مورد نظر شما با موفقیت حذف شد'})
        except PollOptions.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'گزینه ای پیدا نشد'})
    raise Http404("page not found")


def update_poll_option(request, pk, id):
    if request.method == 'POST':
        time.sleep(3)
        poll = get_object_or_404(Poll, pk=pk)
        try:
            poll_option = PollOptions.objects.get(id=id)
            form = PollOptionForm(request.POST, poll=poll, instance=poll_option)
            if form.is_valid():
                form.save()
                body = poll_render_to_string(pk)
                return JsonResponse(
                    {'status': 'success', 'body': body, 'message': 'گزینه مورد نظر شما با موفقیت ویرایش شد'})
            error = 'مشکلی وجود دارد'
            for field in form:
                if field.errors:
                    for error in field.errors:
                        error = error
            return JsonResponse({'status': 'failed', 'message': error})
        except PollOptions.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'گزینه ای پیدا نشد'})
    raise Http404("page not found")
