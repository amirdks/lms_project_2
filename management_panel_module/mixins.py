from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse

from account_module.models import User
from lesson_module.models import Lesson


class JustTeacherMixin(UserPassesTestMixin):
    def test_func(self):
        try:
            lesson = Lesson.objects.get(id=self.kwargs.get('id'))
            if self.request.user.is_teacher and self.request.user.id == lesson.teacher.id:
                return True
            return False
        except Lesson.DoesNotExist:
            if self.request.user.is_teacher:
                return True
            return False


class JustTeacherMixin2(UserPassesTestMixin):
    def test_func(self):
        if self.request.method == 'POST' and not self.request.user.is_teacher:
            return False
        return True


class PermissionMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        users = []
        if not user.is_teacher or not user.is_superuser or not user.is_staff:
            users.append("student")
        elif user.is_superuser:
            users.append("is_superuser")
        elif user.is_staff:
            users.append("is_staff")
        elif user.is_teacher:
            users.append("is_teacher")
        print(users)
        if users[0] not in self.permission_list:
            return False
        return True
