from datetime import datetime
from django.forms import ModelForm
from django import forms
# from .choices import WarehouseChoices, ReportChoices
from .models import Workers


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
            'note': forms.TextInput(attrs = {
                'placeholder': 'Не използвай "/"'
            }),
            'start_date': forms.TextInput(attrs={
                'type': 'date',
            }),
        }

