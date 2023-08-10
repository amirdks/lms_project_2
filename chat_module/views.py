import json
import os

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, Http404, JsonResponse, FileResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views import View

from chat_module.fomrs import FileMessageForm
# Create your views here.
from chat_module.models import Chat, Message, FileMessage
from utils.form_errors import form_error


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


class FileUploadMessageView(LoginRequiredMixin, View):
    def get(self, request, chat_id=None):
        pass

    def post(self, request: HttpRequest, chat_id=None):
        form = FileMessageForm(request.POST, request.FILES)
        chat = Chat.objects.get(unique_code__exact=chat_id, member__user_id=request.user.id)
        if form.is_valid():
            file = form.cleaned_data.get('file_message')
            message = Message.objects.create(chat_id=chat.id, author_id=request.user.id)
            created_file = FileMessage.objects.create(message_id=message.id, file=file)
            file_name = os.path.basename(created_file.file.name)
            chat_room_id = f"chat_{chat.unique_code}"
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                chat_room_id,
                {
                    'type': 'chat_message',
                    'message': json.dumps(
                        {'type': "file", 'sender': request.user.username, 'text': created_file.unique_code,
                         'file_name': file_name}),
                    # 'sender_channel_name': self.channel_name
                })
            return JsonResponse(
                {'status': 'success', 'file_id': created_file.unique_code, 'file_name': file_name})
        else:
            error = form_error(form)
            return JsonResponse({'status': 'failed', 'error': error})


class FileDownloadMessageView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, chat_id=None, file_id=None):
        # file_id = request.POST.get('file_id')
        chat = Chat.objects.get(unique_code__exact=chat_id, member__user_id=request.user.id)
        file = FileMessage.objects.get(unique_code=file_id, message__chat_id=chat.id)
        return FileResponse(file.file, as_attachment=True)

    def post(self, request: HttpRequest, chat_id=None):
        file_id = request.POST.get('file_id')
        chat = Chat.objects.get(unique_code__exact=chat_id, member__user_id=request.user.id)
        file = FileMessage.objects.get(unique_code=file_id, message__chat_id=chat.id)
        return FileResponse(file.file, as_attachment=True)
