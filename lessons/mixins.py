from django.contrib.auth.mixins import UserPassesTestMixin

from account_module.models import User
from lesson_module.models import Lesson


class JustStudentOfLesson(UserPassesTestMixin):
    def test_func(self):
        user: User = self.request.user
        if user.is_teacher:
            return True
        lesson = Lesson.objects.filter(is_active=True, id=self.kwargs.get('id')).first()
        if user.base == lesson.base and user.field_of_study == lesson.field_of_study:
            return True
        return False
