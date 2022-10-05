import time

from celery import shared_task, Celery
from django.contrib import messages

from lms_project_2.celery_conf import app
from account_module.models import User
from utils.email_service import send_email


@app.task()
def send_email_task(users_list, context):
    time.sleep(3)
    send_email(context.get('subject'), users_list, context, template_name='send_email_module/email.html')
    # messages.success(request=self.request, message='با موفقیت قرار گرفت')
    return 'success'