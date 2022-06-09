from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path, reverse


# Register your models here.
admin.site.index_template = "adminlte/info_page.html"
