from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from .scraping import simular_consumo_toner


class Printer(models.Model):
    STATUS_OK = "OK"
    STATUS_UNMONITORED = "NAO_MONITORADA"

    STATUS_CHOICES = (
        (STATUS_OK, "OK"),
        (STATUS_UNMONITORED, "Não monitorada"),
    )

    numero_serie = models.CharField(max_length=200, unique=True)
    ip = models.CharField(max_length=200)
    setor = models.CharField(max_length=200)
    ultima_atualizacao = models.DateTimeField(default=timezone.now)
    nivel_toner = models.IntegerField(
        default=100,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    toner_recem_trocado = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OK)

    class Meta:
        ordering = ["setor"]

    def __str__(self):
        return f"{self.setor} ({self.ip})"

    def update_toner_data(self):
        if self.nivel_toner == 0:
            self.nivel_toner = 100
            self.toner_recem_trocado = True
        else:
            consumo = simular_consumo_toner()
            self.nivel_toner = max(self.nivel_toner - consumo, 0)
            self.toner_recem_trocado = False

        self.status = self.STATUS_OK
        self.ultima_atualizacao = timezone.now()
        self.save()
