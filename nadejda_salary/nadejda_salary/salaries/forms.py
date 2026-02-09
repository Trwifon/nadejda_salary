from datetime import datetime
from django.forms import ModelForm
from django import forms
from .models import Workers, CurrentMonth, WorkerMonth


class WorkerCreateForm(ModelForm):
    class Meta:
        model = Workers
        fields = [
            'name',
            'workshop',
            'contract',
            'start_date',
            'initial_vacation'
        ]

        labels = {
            'name': 'Име',
            'workshop': 'Цех',
            'contract': 'Договор',
            'start_date': 'Започнал на:',
            'initial_vacation': 'Начална отпуска',
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
            'vacation_to_add',
            'salary',
            'vacation_calc',
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
            'bonus_one',
            'bonus_two',
        ]

        labels = {
            'salary': 'Заплата',
            'bonus_one': 'Бонус едно',
            'bonus_two': 'Бонус две',
        }


class WorkerUpdateHRForm(forms.ModelForm):
    class Meta:
        model = Workers
        fields = [
            'end_date',
            'contract',
        ]

        labels = {
            'end_date': 'Напуснал:',
            'contract': 'Договор:',
        }

        widgets = {
            'end_date': forms.TextInput(attrs={
                'type': 'date',
            }),
        }


class DataUpdateForm(forms.ModelForm):
    class Meta:
        model = WorkerMonth
        fields = [
            'paid_by_cash',
        ]

        labels = {
            'paid_by_cash': 'Корекция'
        }


class CloseMonthForm(forms.Form):
    class Meta:
        fields = []