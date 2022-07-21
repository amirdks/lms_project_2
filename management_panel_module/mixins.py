from django.contrib.auth.mixins import UserPassesTestMixin

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
