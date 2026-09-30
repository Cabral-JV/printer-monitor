from django.test import TestCase
from printer_monitor.models import Printer


class PrinterModelTest(TestCase):
    def setUp(self):
        self.printer = Printer.objects.create(
            numero_serie="TEST-0001",
            ip="192.0.2.1",
            setor="Setor de Teste",
        )

    def test_nova_impressora_nasce_com_toner_cheio(self):
        self.assertEqual(self.printer.nivel_toner, 100)

    def test_update_toner_data_reduz_o_nivel(self):
        nivel_antes = self.printer.nivel_toner
        self.printer.update_toner_data()
        self.assertLess(self.printer.nivel_toner, nivel_antes)

    def test_toner_nunca_fica_negativo(self):
        self.printer.nivel_toner = 2
        self.printer.save()

        # Roda a atualizacao varias vezes seguidas para forcar
        # o consumo acumulado a ultrapassar o nivel atual
        for _ in range(10):
            self.printer.update_toner_data()

        self.assertGreaterEqual(self.printer.nivel_toner, 0)

    def test_str_retorna_setor_e_ip(self):
        self.assertEqual(str(self.printer), "Setor de Teste (192.0.2.1)")


def test_toner_reseta_para_100_quando_chega_a_zero(self):
    self.printer.nivel_toner = 0
    self.printer.save()

    self.printer.update_toner_data()

    self.assertEqual(self.printer.nivel_toner, 100)
    self.assertTrue(self.printer.toner_recem_trocado)


def test_notificacao_de_troca_expira_no_ciclo_seguinte(self):
    self.printer.nivel_toner = 0
    self.printer.save()

    self.printer.update_toner_data()  # 1º ciclo: reseta e liga a notificacao
    self.assertTrue(self.printer.toner_recem_trocado)

    self.printer.update_toner_data()  # 2º ciclo: consome normalmente
    self.assertFalse(self.printer.toner_recem_trocado)


def test_toner_recem_trocado_comeca_false(self):
    self.assertFalse(self.printer.toner_recem_trocado)
