import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, Http404
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from django.views import View

# Create your views here.
from account_module.models import User
from chat_module.models import Chat, Message


class ChatView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, chat_id=None):
        user = request.user
        chats = Chat.objects.prefetch_related('message_set', 'member_set').filter(member__user_id=user.id)
        chat = None
        if chat_id:
            try:
                chat = chats.get(unique_code__exact=chat_id, member__user_id=user.id)
                messages = Message.objects.filter(chat_id=chat.id).order_by('date_created')
                context = {'chats': chats, 'current_chat': chat, 'messages': messages,
                           'current_chat_id': mark_safe(json.dumps(chat.unique_code))}
            except Chat.DoesNotExist as e:
                raise Http404('چت مورد نظر شما یافت نشد')
        else:
            context = {'chats': chats}
        return render(request, 'chat_module/chat_list.html', context)
