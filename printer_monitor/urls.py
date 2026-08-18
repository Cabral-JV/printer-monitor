from django.urls import path
from . import views

app_name = "printer_monitor"

urlpatterns = [
    path("", views.printer_list, name="printer_list"),
    path("impressora/<int:pk>/", views.printer_detail, name="printer_detail"),
]