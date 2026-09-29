from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OK)

    class Meta:
        ordering = ["setor"]

    def __str__(self):
        return f"{self.setor} ({self.ip})"
