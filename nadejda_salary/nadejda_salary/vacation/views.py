from django.shortcuts import render

from django.views.generic import ListView, TemplateView

from ..salaries.helpers import worker_month_calc
from ..salaries.models import Workers, WorkerMonth


class VacationListView(ListView):
    model = Workers
    template_name = 'vacation/vacation_list.html'
    context_object_name = 'vacations'


class VacationDisplayView(TemplateView):
    template_name = 'vacation/vacation_display.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        current_worker = Workers.objects.get(pk=pk)

        current_vacation = WorkerMonth.objects.filter(worker=pk).filter(month__open=False)
        for el in current_vacation:
            data = worker_month_calc(current_worker, el)
            print(data.vacation_sum)

        return