from django.db.models.signals import post_save
from django.dispatch import receiver

from notification_module.models import CustomNotification
from poll_module.models import Poll


@receiver(post_save, sender=Poll)
def create_custom_notification(sender, instance, created, **kwargs):
    if created:
        custom_notification = CustomNotification.objects.create(from_teacher_id=instance.from_teacher.id,
                                                                base=instance.base,
                                                                field_of_study=instance.field_of_study,
                                                                title='یک نظر سنجی جدید',
                                                                text=f'یک نظر سنجی جدید با نام {instance.question} قرار گرفت')
        custom_notification.save()
