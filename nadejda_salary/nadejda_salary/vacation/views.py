from django.shortcuts import redirect

from django.views.generic import ListView, TemplateView
from ..salaries.models import Workers, WorkerMonth


class VacationListView(ListView):
    model = Workers
    template_name = 'vacation/vacation_list.html'
    context_object_name = 'vacations'

    def get_queryset(self):
        return Workers.objects.filter(end_date__isnull=True)


class VacationDisplayView(TemplateView):
    template_name = 'vacation/vacation_display.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        current_worker = Workers.objects.get(pk=pk)

        initial_vacation = current_worker.initial_vacation
        given_vacation = initial_vacation

        vacation_all = 0

        current_vacations_data = []

        current_vacation = WorkerMonth.objects.filter(worker=pk).filter(month__open=False)
        for el in current_vacation:
            current_month = {'year': el.month.year,
                             'month': el.month.month,
                             'vacation_used': el.vacation_used,
                             'vacation_calc': el.vacation_calc,
                             'vacation_paid': el.vacation_paid
                             }

            vacation_total = el.vacation_used + el.vacation_calc+el.vacation_paid
            current_month['vacation_total'] = vacation_total
            vacation_all += vacation_total
            current_month['vacation_all'] = vacation_all

            if current_month in (11, 12):
                vacation_to_add = 1.5
            else:
                vacation_to_add = 1.7

            current_month['vacation_to_add'] = vacation_to_add

            given_vacation += vacation_to_add
            current_month['given_vacation'] = given_vacation

            vacation_left = given_vacation - vacation_all
            current_month['vacation_left'] = vacation_left

            current_vacations_data.append(current_month)

            context = {'data': current_vacations_data, 'current_worker': current_worker}

        return context

