from django.contrib.auth.mixins import UserPassesTestMixin

from account_module.models import User
from lesson_module.models import Lesson


class JustTeacherMixin(UserPassesTestMixin):
    def test_func(self):
        return True

