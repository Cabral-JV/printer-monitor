"""
Simulacao de leitura de nivel de toner.

Em um cenario real, este modulo faria uma requisicao HTTP para a impressora
(usando a biblioteca `requests`) e extrairia o nivel de toner da pagina de
status dela (usando `BeautifulSoup`, por exemplo).

Como este projeto roda com IPs ficticios (faixa reservada para documentacao,
RFC 5737) e nao ha impressoras reais acessiveis, esta funcao simula esse
comportamento: em vez de consultar a rede, gera um consumo aleatorio de
toner, como se o equipamento estivesse sendo usado normalmente ao longo
do tempo.
"""

import random


def simular_consumo_toner():
    """Retorna quantos pontos percentuais de toner foram consumidos
    desde a ultima leitura (valor aleatorio, simulando uso real)."""
    return random.randint(1, 8)
