from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AutoprotecaoDoSuperusuarioTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin", password="SenhaForte123!")
        self.outro_usuario = User.objects.create_user(username="outro", password="SenhaForte123!")
        self.client.login(username="admin", password="SenhaForte123!")

    def test_superusuario_nao_consegue_se_autoexcluir(self):
        url = reverse("printer_monitor:user_delete", args=[self.admin.pk])
        self.client.post(url)

        # O usuario ainda deve existir no banco
        self.assertTrue(User.objects.filter(pk=self.admin.pk).exists())

    def test_superusuario_consegue_excluir_outro_usuario(self):
        url = reverse("printer_monitor:user_delete", args=[self.outro_usuario.pk])
        self.client.post(url)

        self.assertFalse(User.objects.filter(pk=self.outro_usuario.pk).exists())

    def test_superusuario_nao_consegue_remover_proprio_status_de_superuser(self):
        url = reverse("printer_monitor:user_update", args=[self.admin.pk])
        self.client.post(url, {
            "username": "admin",
            "email": "admin@example.com",
            "is_active": "on",
            # "is_superuser" ausente de proposito, simulando a caixa desmarcada
        })

        self.admin.refresh_from_db()
        self.assertTrue(self.admin.is_superuser)

    def test_superusuario_nao_consegue_se_autodesativar(self):
        url = reverse("printer_monitor:user_update", args=[self.admin.pk])
        self.client.post(url, {
            "username": "admin",
            "email": "admin@example.com",
            "is_superuser": "on",
            # "is_active" ausente de proposito, simulando a caixa desmarcada
        })

        self.admin.refresh_from_db()
        self.assertTrue(self.admin.is_active)

    def test_superusuario_consegue_editar_outro_usuario_normalmente(self):
        url = reverse("printer_monitor:user_update", args=[self.outro_usuario.pk])
        self.client.post(url, {
            "username": "outro",
            "email": "outro@example.com",
            # sem is_superuser nem is_active: desativando o outro usuario
        })

        self.outro_usuario.refresh_from_db()
        self.assertFalse(self.outro_usuario.is_active)
