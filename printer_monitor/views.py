from django.shortcuts import render, get_object_or_404
from .models import Printer


def printer_list(request):
    printers = Printer.objects.all()
    return render(request, "printer_monitor/printer_list.html", {"printers": printers})


def printer_detail(request, pk):
    printer = get_object_or_404(Printer, pk=pk)
    return render(request, "printer_monitor/printer_detail.html", {"printer": printer})