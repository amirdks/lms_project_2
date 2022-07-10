from django.contrib.auth.mixins import UserPassesTestMixin

from account_module.models import User
from lesson_module.models import Lesson


class JustTeacherMixin(UserPassesTestMixin):
    def test_func(self):
        user: User = self.request.user
        lessos = Lesson.objects.get(id=self.kwargs.get('id'))
        if user.is_teacher and lessos.teacher.id == user.id:
            return True
        return False
