from django.contrib import admin

# Register your models here.
from chat_module.models import Chat, Member, Message, FileMessage


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    pass


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(FileMessage)
class FileMessageAdmin(admin.ModelAdmin):
    pass
