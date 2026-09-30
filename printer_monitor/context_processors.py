from .models import Printer

LIMITE_BAIXO = 10
LIMITE_CRITICO = 5


def notificacoes_toner(request):
    if not request.user.is_authenticated:
        return {}

    notificacoes = []

    for impressora in Printer.objects.filter(toner_recem_trocado=True):
        notificacoes.append({
            "nivel": "success",
            "texto": f"{impressora.setor}: toner trocado, nível restaurado para 100%",
        })

    impressoras_baixas = Printer.objects.filter(
        nivel_toner__lt=LIMITE_BAIXO, toner_recem_trocado=False
    ).order_by("nivel_toner")

    for impressora in impressoras_baixas:
        if impressora.nivel_toner == 0:
            nivel, texto = "danger", f"{impressora.setor}: toner esgotado, é necessário trocar"
        elif impressora.nivel_toner < LIMITE_CRITICO:
            nivel, texto = "danger", f"{impressora.setor}: toner crítico ({impressora.nivel_toner}%)"
        else:
            nivel, texto = "warning", f"{impressora.setor}: toner baixo ({impressora.nivel_toner}%)"

        notificacoes.append({"nivel": nivel, "texto": texto})

    return {
        "notificacoes_toner": notificacoes,
        "total_notificacoes": len(notificacoes),
    }