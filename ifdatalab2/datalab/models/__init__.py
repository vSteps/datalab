# Core
from .campus import Campus
from .grupo_pesquisa import GrupoPesquisa
from .pesquisador import Pesquisador
from .publicacao import Publicacao
from .orientacao import Orientacao
from .projeto_pesquisa import ProjetoPesquisa
from .producao_geral import ProducaoGeral
from .user import AdminGrupo


# Comparador
from .ccsl import PesquisadoresCCSL
from .dgp import PesquisadoresDGP
from .redmine import RedmineCCSL, RedmineDGP
from .comparacoes import CCSLNaoDGP, RedmineNaoDGP
