from django.shortcuts import render, get_object_or_404, redirect
from .models import Printer
from .forms import PrinterForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.core.exceptions import ValidationError
from .forms import CustomUserCreationForm, CustomUserChangeForm


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

    return render(
        request, "printer_monitor/printer_form.html", {"form": form, "printer": printer}
    )


@login_required
def printer_delete(request, pk):
    printer = get_object_or_404(Printer, pk=pk)

    if request.method == "POST":
        printer.delete()
        return redirect("printer_monitor:printer_list")

    return render(
        request, "printer_monitor/printer_confirm_delete.html", {"printer": printer}
    )


def is_superuser(user):
    return user.is_superuser


@login_required
@user_passes_test(is_superuser)
def user_list(request):
    users = User.objects.all()
    return render(request, "printer_monitor/user_list.html", {"users": users})


@login_required
@user_passes_test(is_superuser)
def user_create(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário criado com sucesso.")
            return redirect("printer_monitor:user_list")
    else:
        form = CustomUserCreationForm()

    return render(request, "printer_monitor/user_form.html", {"form": form})


@login_required
@user_passes_test(is_superuser)
def user_update(request, pk):
    user_obj = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=user_obj)
        if form.is_valid():
            # Impede que o único superusuário remova o próprio acesso
            if user_obj == request.user and not form.cleaned_data.get("is_superuser"):
                messages.error(
                    request, "Você não pode remover seu próprio acesso de superusuário."
                )
                return redirect("printer_monitor:user_list")

            form.save()
            messages.success(request, "Usuário atualizado com sucesso.")
            return redirect("printer_monitor:user_list")
    else:
        form = CustomUserChangeForm(instance=user_obj)

    return render(
        request, "printer_monitor/user_form.html", {"form": form, "user_obj": user_obj}
    )


@login_required
@user_passes_test(is_superuser)
def user_delete(request, pk):
    user_obj = get_object_or_404(User, pk=pk)

    if user_obj == request.user:
        messages.error(request, "Você não pode excluir seu próprio usuário.")
        return redirect("printer_monitor:user_list")

    if request.method == "POST":
        user_obj.delete()
        messages.success(request, "Usuário excluído com sucesso.")
        return redirect("printer_monitor:user_list")

    return render(
        request, "printer_monitor/user_confirm_delete.html", {"user_obj": user_obj}
    )


@login_required
@user_passes_test(is_superuser)
def user_change_password(request, pk):
    user_obj = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "As senhas não coincidem.")
            return redirect("printer_monitor:user_update", pk=user_obj.pk)

        try:
            validate_password(new_password, user=user_obj)
        except ValidationError as e:
            messages.error(request, " ".join(e.messages))
            return redirect("printer_monitor:user_update", pk=user_obj.pk)

        user_obj.set_password(new_password)
        user_obj.save()
        messages.success(request, "Senha alterada com sucesso.")
        return redirect("printer_monitor:user_list")

    return redirect("printer_monitor:user_update", pk=user_obj.pk)
