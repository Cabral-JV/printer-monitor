from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


def atualizar_impressoras_agendado():
    from .models import Printer

    impressoras = Printer.objects.all()
    for impressora in impressoras:
        impressora.update_toner_data()

    print(f"[scheduler] {impressoras.count()} impressora(s) atualizada(s).")


def iniciar_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        atualizar_impressoras_agendado,
        trigger=IntervalTrigger(minutes=2),
        id="atualizar_impressoras_job",
        name="Simulacao de consumo de toner",
        replace_existing=True,
    )
    scheduler.start()
