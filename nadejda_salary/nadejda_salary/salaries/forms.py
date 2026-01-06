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
        ]

        labels = {
            'name': 'Име',
            'workshop': 'Цех',
            'contract': 'Договор'
        }

        widgets = {
            'note': forms.TextInput(attrs = {
                'placeholder': 'Не използвай "/"'
            }
        )}

    def clean_note(self):
        current_note = self.cleaned_data.get('note')
        if current_note:
            for letter in current_note:
                if letter == '/':
                    raise forms.ValidationError("Полето не трябва да съдържа символа '//'")
        return current_note