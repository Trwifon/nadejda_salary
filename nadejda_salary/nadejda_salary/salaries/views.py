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

    def get_context_data(self, **kwargs):
        context = {}

        worker_list = Workers.objects.all()
        current_worker = worker_list[0]
        context['worker_list'] = worker_list
        context['worker_pk'] = current_worker

        form = DataFillForm
        context['form'] = form

        return context

    def post(self, request, *args, **kwargs):
        form = DataFillForm(request.POST)
        month_pk = kwargs.get('month_pk')
        current_month = CurrentMonth.objects.get(pk=month_pk)

        worker_pk = kwargs.get('worker_pk')
        current_worker = Workers.objects.get(pk=worker_pk)

        print(current_month, current_worker)

        if form.is_valid():
            worker_mont = form.save(commit=False)

        return HttpResponse()