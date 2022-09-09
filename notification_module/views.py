import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from account_module.models import User
from management_panel_module.mixins import JustTeacherMixin2, PermissionMixin
from notification_module.forms import CustomNotificationForm
from notification_module.models import CustomNotification


# Create your views here.

class NotificationList(JustTeacherMixin2, LoginRequiredMixin, View):

    def get(self, request):
        user: User = request.user
        custom_notifications = CustomNotification.objects.filter(base_id=user.base,
                                                                 field_of_study_id=user.field_of_study)
        if request.user.is_teacher:
            custom_notifications = CustomNotification.objects.filter(from_teacher_id=user.id)

        context = {
            'custom_notifications': custom_notifications
        }
        return render(request, 'notification_module/notification_list.html', context)

    def post(self, request: HttpRequest):
        time.sleep(3)
        try:
            notification = CustomNotification.objects.get(id=request.POST.get('notificationId'))
            notification.delete()
        except CustomNotification.DoesNotExist:
            return JsonResponse(
                {'status': 'danger', 'message': 'اعلان مورد نطر یافت نشد', 'persian_status': 'شکست'})
        custom_notifications = CustomNotification.objects.filter(from_teacher_id=request.user.id)
        body = render_to_string('notification_module/include/notification_list_component.html',
                                context={'custom_notifications': custom_notifications}, request=request)
        return JsonResponse(
            {'status': 'success', 'content': body, 'message': 'اعلان با موفقیت حذف شد', 'persian_status': 'موفق'})


class CreateNotification(LoginRequiredMixin, PermissionMixin, CreateView):
    model = CustomNotification
    form_class = CustomNotificationForm
    template_name = 'notification_module/create_notification.html'
    context_object_name = 'form'
    success_url = reverse_lazy('notification_list')
    permission_list = ['is_teacher', 'is_superuser', 'is_staff']

    def get_form_kwargs(self):
        context = super(CreateNotification, self).get_form_kwargs()
        context['user'] = self.request.user
        return context


class UpdateNotification(LoginRequiredMixin, PermissionMixin, UpdateView):
    model = CustomNotification
    form_class = CustomNotificationForm
    template_name = 'notification_module/create_notification.html'
    context_object_name = 'notification'
    success_url = reverse_lazy('notification_list')
    permission_list = ['is_teacher', 'is_superuser', 'is_staff']

    def get_form_kwargs(self):
        context = super(UpdateNotification, self).get_form_kwargs()
        context['user'] = self.request.user
        return context
