import datetime

from celery import shared_task

from lesson_module.models import SetHomeWork


@shared_task
def discover_expire_home_works():
    SetHomeWork.objects.filter(end_at__lte=datetime.datetime.now()).update(is_finished=True)
