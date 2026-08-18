from django.shortcuts import render, get_object_or_404, redirect
from .models import Printer
from .forms import PrinterForm
from django.contrib.auth.decorators import login_required


def printer_list(request):
    printers = Printer.objects.all()
    return render(request, "printer_monitor/printer_list.html", {"printers": printers})


def printer_detail(request, pk):
    printer = get_object_or_404(Printer, pk=pk)
    return render(request, "printer_monitor/printer_detail.html", {"printer": printer})

@login_required
def printer_create(request):
    if request.method == "POST":
        form = PrinterForm(request.POST)
        if form.is_valid():
            printer = form.save()
            return redirect("printer_monitor:printer_detail", pk=printer.pk)
    else:
        form = PrinterForm()

    return render(request, "printer_monitor/printer_form.html", {"form": form})

@login_required
def printer_update(request, pk):
    printer = get_object_or_404(Printer, pk=pk)

    if request.method == "POST":
        form = PrinterForm(request.POST, instance=printer)
        if form.is_valid():
            form.save()
            return redirect("printer_monitor:printer_detail", pk=printer.pk)
    else:
        form = PrinterForm(instance=printer)

    return render(request, "printer_monitor/printer_form.html", {"form": form, "printer": printer})

@login_required
def printer_delete(request, pk):
    printer = get_object_or_404(Printer, pk=pk)

    if request.method == "POST":
        printer.delete()
        return redirect("printer_monitor:printer_list")

    return render(request, "printer_monitor/printer_confirm_delete.html", {"printer": printer})