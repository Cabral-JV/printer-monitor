from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from printer_monitor.models import Printer


class PrinterCreateTest(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username="usuario", password="SenhaForte123!")
        self.client.login(username="usuario", password="SenhaForte123!")

    def test_post_valido_cria_impressora(self):
        url = reverse("printer_monitor:printer_create")
        self.client.post(url, {
            "setor": "Setor Novo",
            "ip": "192.0.2.50",
            "numero_serie": "DEMO-9001",
            "status": Printer.STATUS_OK,
        })

        self.assertTrue(Printer.objects.filter(numero_serie="DEMO-9001").exists())

    def test_impressora_criada_nasce_com_toner_cheio(self):
        url = reverse("printer_monitor:printer_create")
        self.client.post(url, {
            "setor": "Setor Novo",
            "ip": "192.0.2.51",
            "numero_serie": "DEMO-9002",
            "status": Printer.STATUS_OK,
        })

        printer = Printer.objects.get(numero_serie="DEMO-9002")
        self.assertEqual(printer.nivel_toner, 100)

    def test_post_invalido_nao_cria_impressora(self):
        url = reverse("printer_monitor:printer_create")
        quantidade_antes = Printer.objects.count()

        self.client.post(url, {
            "setor": "",  # campo obrigatorio vazio, de proposito
            "ip": "192.0.2.52",
            "numero_serie": "DEMO-9003",
            "status": Printer.STATUS_OK,
        })

        self.assertEqual(Printer.objects.count(), quantidade_antes)

    def test_get_na_view_de_criacao_nao_e_permitido(self):
        url = reverse("printer_monitor:printer_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)


class PrinterUpdateDeleteTest(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username="usuario", password="SenhaForte123!")
        self.client.login(username="usuario", password="SenhaForte123!")

        self.printer = Printer.objects.create(
            numero_serie="DEMO-8001",
            ip="192.0.2.60",
            setor="Setor Original",
        )

    def test_post_valido_atualiza_impressora(self):
        url = reverse("printer_monitor:printer_update", args=[self.printer.pk])
        self.client.post(url, {
            "setor": "Setor Atualizado",
            "ip": self.printer.ip,
            "numero_serie": self.printer.numero_serie,
            "status": Printer.STATUS_OK,
        })

        self.printer.refresh_from_db()
        self.assertEqual(self.printer.setor, "Setor Atualizado")

    def test_atualizar_nao_altera_nivel_de_toner(self):
        # Garante que editar setor/IP/status nao mexe no toner,
        # que so deve mudar via update_toner_data()
        self.printer.nivel_toner = 42
        self.printer.save()

        url = reverse("printer_monitor:printer_update", args=[self.printer.pk])
        self.client.post(url, {
            "setor": "Setor Atualizado",
            "ip": self.printer.ip,
            "numero_serie": self.printer.numero_serie,
            "status": Printer.STATUS_OK,
        })

        self.printer.refresh_from_db()
        self.assertEqual(self.printer.nivel_toner, 42)

    def test_post_exclui_impressora(self):
        url = reverse("printer_monitor:printer_delete", args=[self.printer.pk])
        self.client.post(url)

        self.assertFalse(Printer.objects.filter(pk=self.printer.pk).exists())

    def test_get_na_view_de_exclusao_nao_e_permitido(self):
        url = reverse("printer_monitor:printer_delete", args=[self.printer.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

    def test_visitante_deslogado_nao_consegue_excluir(self):
        self.client.logout()
        url = reverse("printer_monitor:printer_delete", args=[self.printer.pk])
        self.client.post(url)

        # A impressora deve continuar existindo
        self.assertTrue(Printer.objects.filter(pk=self.printer.pk).exists())
