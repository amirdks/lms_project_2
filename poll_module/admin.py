from django.contrib import admin

from poll_module.models import Poll, PollOptions

# Register your models here.

admin.site.register(Poll)
admin.site.register(PollOptions)