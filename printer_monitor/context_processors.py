from .models import Printer

LIMITE_BAIXO = 10
LIMITE_CRITICO = 5


def notificacoes_toner(request):
    """Disponibiliza a lista de alertas de toner em todos os templates,
    sem precisar que cada view passe isso manualmente no contexto."""

    if not request.user.is_authenticated:
        return {}

    impressoras_baixas = Printer.objects.filter(nivel_toner__lt=LIMITE_BAIXO).order_by(
        "nivel_toner"
    )

    notificacoes = []
    for impressora in impressoras_baixas:
        if impressora.nivel_toner == 0:
            nivel = "danger"
            texto = f"{impressora.setor}: toner esgotado, é necessário trocar"
        elif impressora.nivel_toner < LIMITE_CRITICO:
            nivel = "danger"
            texto = f"{impressora.setor}: toner crítico ({impressora.nivel_toner}%)"
        else:
            nivel = "warning"
            texto = f"{impressora.setor}: toner baixo ({impressora.nivel_toner}%)"

        notificacoes.append({"nivel": nivel, "texto": texto})

    return {
        "notificacoes_toner": notificacoes,
        "total_notificacoes": len(notificacoes),
    }
