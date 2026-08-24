from django.views.generic import ListView, TemplateView
from .helpers import vacation_calc
from ..salaries.models import Workers


class VacationListView(ListView):
    model = Workers
    template_name = 'vacation/vacation_list.html'
    context_object_name = 'workers'

    def get_queryset(self):
        return Workers.objects.filter(end_date__isnull=True).filter(contract=True).order_by('workshop', 'name')


class VacationDisplayView(TemplateView):
    template_name = 'vacation/vacation_display.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        current_worker = Workers.objects.get(pk=pk)

        context = vacation_calc(current_worker)

        return context

