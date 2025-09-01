import datetime
from django.core.management.base import BaseCommand
from django.db import connections
from django.contrib.auth.models import User
from datalab.models import Campus, Pesquisador, Publicacao, Orientacao, ProjetoPesquisa, ProducaoGeral

class Command(BaseCommand):
    help = 'Migra dados do banco de dados legado (antigo) para os novos modelos Django.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('== INICIANDO MIGRAÇÃO DE DADOS =='))

        # PASSO 1: Criar objetos essenciais que não dependem de outros dados.
        self.stdout.write("\n1. Criando Campi...")
        campus_cnat, _ = Campus.objects.get_or_create(nome_campus="CNAT")
        campus_caico, _ = Campus.objects.get_or_create(nome_campus="Caicó")
        self.stdout.write(self.style.SUCCESS('   - Campi criados/verificados.'))

        with connections['legacy'].cursor() as cursor:

            # PASSO 2: Migrar Perfis de Pesquisadores.
            self.stdout.write("\n2. Migrando Perfis de Pesquisadores...")
            cursor.execute("SELECT nome_completo, idlattes, funcao, campus_id FROM pesquisadores")
            for row in cursor.fetchall():
                nome, idlattes, funcao, campus_id_antigo = row
                
                campus_novo = campus_cnat if campus_id_antigo == 1 else campus_caico
                
                Pesquisador.objects.update_or_create(
                    idlattes=idlattes,
                    defaults={
                        'nome_completo': nome,
                        'funcao': funcao or 'Aluno',  
                        'campus': campus_novo,
                    }
                )
            self.stdout.write(self.style.SUCCESS(f'   - {Pesquisador.objects.count()} perfis de pesquisadores migrados.'))

            # PASSO 3: Migrar Publicações (juntando CNAT e Caicó).
            self.stdout.write("\n3. Migrando Publicações...")
            for campus_obj, tabela_antiga in [(campus_cnat, 'publicacoes_cnat'), (campus_caico, 'publicacoes_caico')]:
                self.stdout.write(f'   - Lendo de {tabela_antiga}...')
                cursor.execute(f"SELECT autor, publicacao, categoria, subcategoria, ccsl FROM {tabela_antiga}")
                for row in cursor.fetchall():
                    autor_nome, titulo, categoria, subcategoria, ccsl = row
                    try:
                        pesquisador = Pesquisador.objects.get(nome_completo=autor_nome)
                        Publicacao.objects.get_or_create(
                            pesquisador=pesquisador,
                            titulo=titulo,
                            defaults={
                                'campus': campus_obj,
                                'categoria': categoria,
                                'subcategoria': subcategoria,
                                'ccsl': bool(ccsl)
                            }
                        )
                    except Pesquisador.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'     - Aviso: Pesquisador "{autor_nome}" não encontrado. Pulando publicação.'))
            self.stdout.write(self.style.SUCCESS(f'   - {Publicacao.objects.count()} publicações migradas.'))

            # PASSO 4: Migrar Orientações (juntando CNAT e Caicó).
            self.stdout.write("\n4. Migrando Orientações...")
            for campus_obj, tabela_antiga in [(campus_cnat, 'orientacoes_cnat'), (campus_caico, 'orientacoes_caico')]:
                 self.stdout.write(f'   - Lendo de {tabela_antiga}...')
                 cursor.execute(f"SELECT autor, orientacao FROM {tabela_antiga}")
                 for row in cursor.fetchall():
                    autor_nome, titulo = row
                    try:
                        pesquisador = Pesquisador.objects.get(nome_completo=autor_nome)
                        Orientacao.objects.get_or_create(
                            pesquisador=pesquisador,
                            titulo=titulo,
                            defaults={'campus': campus_obj}
                        )
                    except Pesquisador.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'     - Aviso: Pesquisador "{autor_nome}" não encontrado. Pulando orientação.'))
            self.stdout.write(self.style.SUCCESS(f'   - {Orientacao.objects.count()} orientações migradas.'))


            # PASSO 5: Migrar Produções Gerais (juntando CNAT e Caicó).
            self.stdout.write("\n5. Migrando Resumo de Produções...")
            for campus_obj, tabela_antiga in [(campus_cnat, 'producoes_gerais_cnat'), (campus_caico, 'producoes_gerais_caico')]:
                self.stdout.write(f'   - Lendo de {tabela_antiga}...')
                cursor.execute(f"SELECT autor, ultima_atualizacao, producoes_tecnicas, producoes_bibliograficas, orientacoes, projetos_pesquisa FROM {tabela_antiga}")
                for row in cursor.fetchall():
                    autor_nome, data_str, p_tec, p_bib, ori, p_pesq = row
                    try:
                        pesquisador = Pesquisador.objects.get(nome_completo=autor_nome)
                        
                        data_atualizacao = None
                        if data_str:
                            try:
                                data_atualizacao = datetime.datetime.strptime(data_str, '%d/%m/%Y')
                            except (ValueError, TypeError):
                                pass

                        ProducaoGeral.objects.update_or_create(
                            pesquisador=pesquisador,
                            defaults={
                                'campus': campus_obj,
                                'ultima_atualizacao': data_atualizacao,
                                'producoes_tecnicas': p_tec or 0,
                                'producoes_bibliograficas': p_bib or 0,
                                'orientacoes': ori or 0,
                                'projetos_pesquisa': p_pesq or 0,
                            }
                        )
                    except Pesquisador.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'     - Aviso: Pesquisador "{autor_nome}" não encontrado. Pulando produções.'))
            self.stdout.write(self.style.SUCCESS(f'   - {ProducaoGeral.objects.count()} resumos de produção migrados.'))


        self.stdout.write(self.style.SUCCESS('\n== MIGRAÇÃO CONCLUÍDA COM SUCESSO! =='))
        self.stdout.write('Pode agora executar "python manage.py runserver" e verificar os dados no Admin.')

