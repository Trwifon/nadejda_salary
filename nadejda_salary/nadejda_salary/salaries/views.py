from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, FormView, UpdateView, DeleteView
from nadejda_salary.salaries.models import Workers
from nadejda_salary.salaries.forms import WorkerCreateForm


# class WorkerCreateView(PermissionRequiredMixin, CreateView):
class WorkerCreateView(CreateView):
    model = Workers
    form_class = WorkerCreateForm
    template_name = 'workers/worker_create.html'
    success_url = reverse_lazy('dashboard')
    # permission_required = ('records.add_partner',)
