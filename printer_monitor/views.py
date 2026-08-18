from django.shortcuts import render
from .models import Printer


def printer_list(request):
    printers = Printer.objects.all()
    return render(request, "printer_monitor/printer_list.html", {"printers": printers})