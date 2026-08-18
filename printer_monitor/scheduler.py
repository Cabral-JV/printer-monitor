from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


def atualizar_impressoras_agendado():
    from .models import Printer  # import local evita problema de dependencia circular

    impressoras = Printer.objects.all()
    for impressora in impressoras:
        impressora.update_toner_data()

    print(f"[scheduler] {impressoras.count()} impressora(s) verificada(s).")


def iniciar_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        atualizar_impressoras_agendado,
        trigger=CronTrigger(hour=15, day_of_week="mon-fri"),
        id="atualizar_impressoras_job",
        name="Atualizacao automatica das impressoras",
        replace_existing=True,
    )
    scheduler.start()
