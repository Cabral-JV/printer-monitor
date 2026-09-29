import random

from django.core.management.base import BaseCommand
from printer_monitor.models import Printer

SETORES = [
    "Biblioteca",
    "Secretaria Academica",
    "Laboratorio de Informatica",
    "Coordenacao de Curso",
    "Diretoria Geral",
    "Setor Financeiro",
    "Recursos Humanos",
    "Sala dos Professores",
]


class Command(BaseCommand):
    help = "Popula o banco com impressoras ficticias para fins de demonstracao."

    def add_arguments(self, parser):
        parser.add_argument(
            "--quantidade",
            type=int,
            default=len(SETORES),
            help="Quantidade de impressoras ficticias a criar.",
        )

    def handle(self, *args, **options):
        quantidade = options["quantidade"]

        if quantidade > 254:
            self.stderr.write(
                "Maximo de 254 impressoras (limite da faixa de IP de exemplo)."
            )
            return

        criadas = 0

        for i in range(quantidade):
            setor = SETORES[i % len(SETORES)]
            ip = f"192.0.2.{i + 1}"
            numero_serie = f"DEMO-{1000 + i}"

            _, foi_criado = Printer.objects.get_or_create(
                numero_serie=numero_serie,
                defaults={
                    "ip": ip,
                    "setor": setor,
                    "status": Printer.STATUS_OK,
                    "nivel_toner": random.randint(5, 100),
                },
            )

            if foi_criado:
                criadas += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{criadas} impressora(s) ficticia(s) criada(s) com sucesso."
            )
        )
