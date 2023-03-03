import os
import random

from django.db import models

from utils.unique_code_generator import id_generator


# Create your models here.
def unique_generator(length=10):
    source = "abcdefghijklmnopqrztuvwxyz"
    result = ""
    for _ in range(length):
        result += source[random.randint(0, length)]
    return result


# Create your models here.
# class GroupChat(models.Model):
#     title = models.CharField(max_length=50)
#     unique_code = models.CharField(max_length=10, default=unique_generator)
#     date_created = models.DateTimeField(auto_now_add=True)
#
#
# class Member(models.Model):
#     chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
#     user = models.ForeignKey('account_module.User', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.user.username
#


class Chat(models.Model):
    unique_code = models.CharField(max_length=10, default=unique_generator, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey('account_module.User', on_delete=models.CASCADE)
    text = models.TextField(default="")
    date_created = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False, verbose_name='سین شده')


class Member(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey('account_module.User', on_delete=models.CASCADE)


class ImageMessage(models.Model):
    message = models.OneToOneField('Message', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/chat', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)


class FileMessage(models.Model):
    message = models.OneToOneField('Message', on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/chat', blank=True, null=True)
    unique_code = models.CharField(max_length=10, default=id_generator, unique=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.file.name)
