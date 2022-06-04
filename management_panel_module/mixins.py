from django.contrib.auth.mixins import UserPassesTestMixin

from account_module.models import User


class JustTeacherMixin(UserPassesTestMixin):
    def test_func(self):
        user: User = self.request.user
        if user.is_teacher:
            return True
        return False
