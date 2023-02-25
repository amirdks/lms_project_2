from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse

from account_module.models import User


class CustomAuthentication:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: HttpRequest):
        # user: User = request.user
        # if 'admin' not in request.build_absolute_uri():
        #     try:
        #         if not user.is_teacher and (user.is_staff or user.is_superuser):
        #             return redirect(reverse('admin:index'))
        #     except:
        #         pass
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
