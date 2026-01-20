from datetime import datetime
from django.forms import ModelForm
from django import forms
# from .choices import WarehouseChoices, ReportChoices
from .models import Workers, CurrentMonth, WorkerMonth


class WorkerCreateForm(ModelForm):
    class Meta:
        model = Workers
        fields = [
            'name',
            'workshop',
            'contract',
            'start_date',
        ]

        labels = {
            'name': 'Име',
            'workshop': 'Цех',
            'contract': 'Договор',
            'start_date': 'Започнал на:'
        }

        widgets = {
            'start_date': forms.TextInput(attrs={
                'type': 'date',
            }),
        }


class MonthCreateForm(ModelForm):
    class Meta:
        model = CurrentMonth
        fields = [
            'year',
            'month',
            'work_days',
        ]

        labels = {
            'year': 'Година',
            'month': 'Месец',
            'work_days': 'Работни дни',
        }


class DataFillForm(ModelForm):
    class Meta:
        model = WorkerMonth
        exclude = [
            'worker',
            'month',
        ]

        labels = {
            'insurance': 'Осигуровки',
            'work_hours': 'Изработени часове',
            'sick_days_noi': 'Болн. дни от НОИ',
            'sick_days_firm': 'Болн. дни от фирмата',
            'vacation_used': 'Използвана отпуска',
            'vacation_paid': 'Изплатена отпуска',
            'paid_by_bank': 'Изплатени по банка',
            'paid_by_cash': 'Изплатени в брой',
            'mobile': 'Сметка GSM',
            'voucher': 'Ваучери',
        }


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Workers
        fields = [
            'salary',
        ]

        labels = {
            'salary': 'Заплата',
        }


class WorkerUpdateHRForm(forms.ModelForm):
    class Meta:
        model = Workers
        fields = [
            'end_date',
        ]

        labels = {
            'end_date': 'Напуснал:',
        }

        widgets = {
            'end_date': forms.TextInput(attrs={
                'type': 'date',
            }),
        }

