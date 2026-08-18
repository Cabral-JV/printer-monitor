from django.urls import path
from . import views

app_name = "printer_monitor"

urlpatterns = [
    path("", views.printer_list, name="printer_list"),
    path("impressora/<int:pk>/", views.printer_detail, name="printer_detail"),
    path("impressora/nova/", views.printer_create, name="printer_create"),
    path("impressora/<int:pk>/editar/", views.printer_update, name="printer_update"),
    path("impressora/<int:pk>/excluir/", views.printer_delete, name="printer_delete"),
    path("usuarios/", views.user_list, name="user_list"),
    path("usuarios/novo/", views.user_create, name="user_create"),
    path("usuarios/<int:pk>/editar/", views.user_update, name="user_update"),
    path("usuarios/<int:pk>/excluir/", views.user_delete, name="user_delete"),
    path("usuarios/<int:pk>/senha/", views.user_change_password, name="user_change_password"),
]