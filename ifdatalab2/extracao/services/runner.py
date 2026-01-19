# extracao/services/runner.py
import threading
from extracao.models import Extracao
from extracao.services.lattes_extrator import extrair_novo_pesquisador


def _rodar_extracao(extracao_id):
    extracao = Extracao.objects.get(id=extracao_id)
    extracao.status = "RODANDO"
    extracao.save()

    try:
        p = extracao.pesquisador
        extrair_novo_pesquisador(
            nome=p.nome_completo,
            lattes_id=p.idlattes,
            campus_nome=p.campus.nome_campus
        )
        extracao.status = "SUCESSO"
    except Exception as e:
        extracao.status = "ERRO"
        extracao.erro = str(e)

    extracao.save()


def disparar_extracao(extracao):
    thread = threading.Thread(
        target=_rodar_extracao,
        args=(extracao.id,),
        daemon=True
    )
    thread.start()
