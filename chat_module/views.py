import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views import View

# Create your views here.
from account_module.models import User


class ChatList(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        user: User = request.user
        users = User.objects.filter(base_id=user.base, field_of_study_id=user.field_of_study_id).exclude(id=user.id)
        context = {'users': users}
        return render(request, 'chat_module/chat_list.html', context)


class ChatPv(View):
    def get(self, request, username):
        context = {'username': mark_safe(json.dumps(username))}
        return render(request, 'chat_module/chat_box.html', context)
