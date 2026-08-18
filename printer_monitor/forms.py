from django import forms
from .models import Printer


class PrinterForm(forms.ModelForm):
    class Meta:
        model = Printer
        fields = ["setor", "ip", "numero_serie", "status", "data_remaining"]
