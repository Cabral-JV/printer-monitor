from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class LoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="usuario_teste", password="SenhaForte123!")

    def test_login_com_credenciais_corretas_funciona(self):
        login_ok = self.client.login(username="usuario_teste", password="SenhaForte123!")
        self.assertTrue(login_ok)

    def test_login_com_senha_errada_falha(self):
        login_ok = self.client.login(username="usuario_teste", password="senha_errada")
        self.assertFalse(login_ok)

    def test_pagina_de_login_carrega(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)


class AcessoRestritoTest(TestCase):
    def setUp(self):
        self.usuario_comum = User.objects.create_user(username="comum", password="SenhaForte123!")
        self.superusuario = User.objects.create_superuser(username="admin", password="SenhaForte123!")

    def test_visitante_deslogado_e_redirecionado_ao_criar_impressora(self):
        response = self.client.get(reverse("printer_monitor:printer_create"))
        self.assertEqual(response.status_code, 302)

    def test_usuario_comum_nao_acessa_lista_de_usuarios(self):
        self.client.login(username="comum", password="SenhaForte123!")
        response = self.client.get(reverse("printer_monitor:user_list"))
        self.assertEqual(response.status_code, 302)

    def test_superusuario_acessa_lista_de_usuarios(self):
        self.client.login(username="admin", password="SenhaForte123!")
        response = self.client.get(reverse("printer_monitor:user_list"))
        self.assertEqual(response.status_code, 200)

    def test_visitante_deslogado_consegue_ver_listagem_publica(self):
        response = self.client.get(reverse("printer_monitor:printer_list"))
        self.assertEqual(response.status_code, 200)
