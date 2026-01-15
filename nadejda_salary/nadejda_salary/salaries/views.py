from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, FormView, UpdateView, DeleteView
from .models import Workers, CurrentMonth, WorkerMonth
from .forms import WorkerCreateForm, MonthCreateForm, DataFillForm


class WorkerCreateView(PermissionRequiredMixin, CreateView):
    model = Workers
    form_class = WorkerCreateForm
    template_name = 'workers/worker_create.html'
    success_url = reverse_lazy('dashboard')
    permission_required = ('salaries.add_workers',)


class MonthCreateView(PermissionRequiredMixin, CreateView):
    model = CurrentMonth
    form_class = MonthCreateForm
    template_name = 'months/month_create.html'
    success_url = reverse_lazy('dashboard')
    permission_required = ('salaries.add_currentmonth',)

    def get(self, request, *args, **kwargs):
        form = self.form_class

        open_month = CurrentMonth.objects.filter(open=True)
        if open_month:
            return HttpResponse('Имате неприключен месец.')

        return render(request, 'months/month_create.html', {
            'form': form,
        })


class DataFillView(PermissionRequiredMixin, CreateView):
    model = WorkerMonth
    form_class = DataFillForm
    template_name = 'workers/data.html'
    permission_required = 'salaries.add_workermonth'

    def get_context_data(self, *args, **kwargs):
        context = {}

        current_month = CurrentMonth.objects.get(open=True)

        workers = Workers.objects.filter(end_date=None)

        worker_list = WorkerMonth.objects.filter(month=current_month)

        if not worker_list:
            for next_worker in workers:
                new_data = WorkerMonth(
                    insurance=0,
                    work_hours=0,
                    sick_days_noi=0,
                    sick_days_firm=0,
                    vacation_used=0,
                    vacation_paid=0,
                    paid_by_bank=0,
                    paid_by_cash=0,
                    mobile=0,
                    voucher=0,
                    worker=next_worker,
                    month=current_month,
                )
                new_data.save()

        worker_list = WorkerMonth.objects.filter(month=current_month)
        context['worker_list'] = worker_list

        form = DataFillForm
        context['form'] = form

        return context

    def post(self, request, *args, **kwargs):
        form = DataFillForm(request.POST)
        month_pk = kwargs.get('month_pk')
        current_month = CurrentMonth.objects.get(pk=month_pk)

        worker_pk = kwargs.get('worker_pk')
        current_worker = Workers.objects.get(pk=worker_pk)

        if form.is_valid():
            worker_month = form.save(commit=False)

        return HttpResponse()