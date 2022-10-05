from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View
# from django.views import View
from django.views.generic import ListView

from account_module.models import User
from lessons.models import Base
from management_panel_module.mixins import PermissionMixin
from send_email_module.filters import QuizResultFilter
from send_email_module.forms import EmailForm
from send_email_module.models import LinkEmailFile, Email
from send_email_module.tasks import send_email_task
from utils.form_errors import form_error
# Create your views here.
class SendEmail(LoginRequiredMixin, PermissionMixin, View):
    permission_list = ['is_teacher', 'is_staff', 'is_superuser']
    form_class = EmailForm

    def get(self, request):
        context = {'form': self.form_class}
        return render(request, 'send_email_module/main_page.html', context)

    def post(self, request: HttpRequest):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            files = request.FILES
            for file_name, file in files.items():
                if file_name.startswith('file'):
                    LinkEmailFile.objects.create(file=file, email_id=instance.id)
            users = User.objects.filter(field_of_study_id=instance.field_of_study, base_id=instance.base.id,
                                        is_teacher=False).values_list('email')
            users_list = [item for t in users for item in t]
            context = {
                'subject': instance.subject,
                'content': instance.content,
                'from_teacher': instance.from_teacher.get_full_name(),
                'base': instance.base.__str__(),
                'field_of_study': instance.field_of_study.__str__(),
                'files': [file.file.url for file in LinkEmailFile.objects.filter(email_id=instance.id)]
            }
            send_email_task.apply_async(args=[users_list, context])
            return JsonResponse({'status': 'success', 'message': 'ایمیل ها به زودی ارسال میشوند'})
        return JsonResponse({'status': 'failed', 'message': form_error(form)})


class EmailList(LoginRequiredMixin, PermissionMixin, ListView):
    model = Email
    template_name = 'send_email_module/email_list.html'
    context_object_name = 'emails'
    ordering = 'send_at'
    permission_list = ['is_teacher', 'is_superuser', 'is_staff']

    def get_queryset(self):
        query = super(EmailList, self).get_queryset()
        query = query.filter(from_teacher_id=self.request.user.id)
        # if self.request.GET.get('base'):
        query = QuizResultFilter(self.request.GET, queryset=query).qs
        return query

    def post(self, request):
        search = request.POST.get('table_search')
        query = self.get_queryset()
        query = query.filter(Q(subject__contains=search) | Q(content__contains=search))
        body = render_to_string('send_email_module/includes/email_list_content.html', context={'emails': query})
        return JsonResponse({'body': body})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EmailList, self).get_context_data(object_list=None, **kwargs)
        context['filter'] = QuizResultFilter(self.request.GET, queryset=Base.objects.all())
        return context
