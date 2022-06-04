from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from site_module.models import SiteSetting


class HomeView(TemplateView):
    template_name = 'home_module/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['site_setting'] = SiteSetting.objects.filter(is_main_setting=True).first()
        return context


def site_header_component(request):
    return render(request, 'shared/site_header_component.html')


def site_footer_component(request):
    context = {
        'site_setting': SiteSetting.objects.filter(is_main_setting=True).first()
    }
    return render(request, 'shared/site_footer_component.html', context)


def not_found(request, exception):
    return render(request, '404.html')
