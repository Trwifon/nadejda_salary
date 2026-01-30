from django.shortcuts import render

from django.views.generic import ListView
from nadejda_salary.salaries.models import Workers

class VacationListView(ListView):
    model = Workers
    template_name = 'vacation/vacation_list.html'
    context_object_name = 'vacations'
