from django.http import HttpResponse
from .models import Printer


def printer_list(request):
    printers = Printer.objects.all()
    texto = "\n".join(str(p) for p in printers) or "Nenhuma impressora cadastrada ainda."
    return HttpResponse(texto, content_type="text/plain")