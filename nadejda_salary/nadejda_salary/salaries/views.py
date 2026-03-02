from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DetailView
from .models import Workers, CurrentMonth, WorkerMonth
from .forms import WorkerCreateForm, MonthCreateForm, \
    DataFillForm, WorkerUpdateForm, WorkerUpdateHRForm,\
    DataUpdateForm, CloseMonthForm


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
            return render(request, 'months/month_unclosed.html')

        return render(request, 'months/month_create.html', {
            'form': form,
        })


class DataFillView(PermissionRequiredMixin, TemplateView):
    model = WorkerMonth
    template_name = 'worker_month/data.html'
    permission_required = 'salaries.add_workermonth'

    def get_context_data(self, *args, **kwargs):
        index = self.kwargs['index']
        context = {}

        current_month = CurrentMonth.objects.get(open=True)
        month = current_month.month
        year = current_month.year

        workers = Workers.objects.filter(
            Q(end_date__isnull=True) |
            Q(end_date__month=month, end_date__year=year)
        )

        worker_month_list = WorkerMonth.objects.\
            filter(month=current_month).\
            order_by('worker__workshop', 'worker__name')

        workers_id_list = [el.worker for el in worker_month_list]

        for next_worker in workers:
            if next_worker not in workers_id_list:
                new_data = WorkerMonth(
                    insurance=0,
                    work_hours=0,
                    sick_days_noi=0,
                    sick_days_firm=0,
                    vacation_to_add=0,
                    vacation_used=0,
                    vacation_paid=0,
                    paid_by_bank=0,
                    paid_by_cash=0,
                    mobile=0,
                    voucher=0,
                    worker=next_worker,
                    month=current_month,
                    vacation_calc = 0,
                )
                new_data.save()

        worker_month_list = WorkerMonth.objects.\
            filter(month=current_month).\
            order_by('worker__workshop', 'worker__name')
        context['worker_month_list'] = worker_month_list

        current_data = worker_month_list[index]
        context['current_data'] = current_data

        form = DataFillForm
        context['form'] = form(instance=current_data)

        return context

    def post(self, request, **kwargs):
        index = kwargs.get('index')
        current_month = CurrentMonth.objects.get(open=True)
        worker_month_list = WorkerMonth.objects.\
            filter(month=current_month).\
            order_by('worker__workshop', 'worker__name')

        worker_list_length = len(worker_month_list) - 1

        row_pk = worker_month_list[index].id

        data = get_object_or_404(WorkerMonth, pk=row_pk)
        form = DataFillForm(request.POST, instance=data)

        if form.is_valid():
            form.save()

        if 'Next' in request.POST:
            index = index + 1 if index < worker_list_length else index

        if 'Previous' in request.POST:
            index = index - 1 if index > 0 else index

        return redirect('data', index)


class WorkerUpdateView(PermissionRequiredMixin, TemplateView):
    model = Workers
    template_name = 'workers/worker_update.html'
    permission_required = 'salaries.change_workers'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = {}

        index = kwargs.get('index')
        context['index'] = index

        worker_list = Workers.objects.filter(end_date=None).order_by('workshop', 'name')
        context['worker_list'] = worker_list

        current_worker = worker_list[index]
        context['current_worker'] = current_worker

        if user.is_staff:
            form = WorkerUpdateForm
        else:
            form = WorkerUpdateHRForm

        context['form'] = form(instance=current_worker)

        return context

    def post(self, request, **kwargs):
        user = self.request.user
        index = kwargs.get('index')

        worker_list = Workers.objects.filter(end_date=None).order_by('workshop', 'name')
        worker_pk = worker_list[index].id

        length = len(worker_list) -1

        worker = get_object_or_404(Workers, id=worker_pk)

        if user.is_staff:
            form = WorkerUpdateForm(request.POST, instance=worker)
        else:
            form = WorkerUpdateHRForm(request.POST, instance=worker)

        if form.is_valid():
            form.save()

        if 'Next' in request.POST:
            index = index + 1 if index < length else index

        if 'Previous' in request.POST:
            index = index - 1 if index > 0 else index

        return redirect('update_worker', index)


class DataListView(PermissionRequiredMixin, ListView):
    model = WorkerMonth
    template_name = 'worker_month/data_list.html'
    permission_required = 'salaries.change_workermonth'
    context_object_name = 'workers'

    def get_queryset(self):
        self.current_month = CurrentMonth.objects.get(open=True)

        worker_month_list = (
            WorkerMonth.objects
            .select_related('worker', 'month')
            .filter(month=self.current_month)
            .order_by('worker__workshop', 'worker__name')
        )

        for worker in worker_month_list:
            worker.salary = worker.worker.salary
            worker.bonus_one = worker.worker.bonus_one
            worker.bonus_two = worker.worker.bonus_two
            worker.save()

        return worker_month_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_month'] = self.current_month
        return context




class DataUpdateView(PermissionRequiredMixin, UpdateView):
    model = WorkerMonth
    form_class = DataUpdateForm
    template_name = 'worker_month/data_update.html'
    permission_required = 'salaries.change_workers'
    success_url = reverse_lazy('list_data')

    def get_context_data(self, **kwargs):
        context = {}

        form = DataUpdateForm(instance=self.object)
        current_data = WorkerMonth.objects.get(pk=self.kwargs['pk'])

        context['form'] = form
        context['current_data'] = current_data

        return context

    def post(self, request, *args, **kwargs):
        form = DataUpdateForm(request.POST)
        self.object = self.get_object()

        if form.is_valid():
            self.object.save()

        return super().post(request, *args, **kwargs)


class CloseMonthView(TemplateView):
    template_name = 'months/month_close.html'
    success_url = reverse_lazy('list_data')

    def get_context_data(self, **kwargs):
        context = {}

        month = CurrentMonth.objects.get(pk=self.kwargs['pk'])
        context['current_month'] = month

        return context

    def post(self, request,  **kwargs):
        pk = kwargs.get('pk')
        form = CloseMonthForm(request.POST)

        if form.is_valid:
            if 'yes' in request.POST:
                month = CurrentMonth.objects.get(pk=pk)
                month.open = False
                month.save()
            else:
                return redirect('dashboard')

        return redirect('dashboard')


class DetailsWorkerMonthView(PermissionRequiredMixin, DetailView):
    model = WorkerMonth
    template_name = 'worker_month/details_worker_month.html'
    permission_required = 'salaries.change_workers'











