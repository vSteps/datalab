from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep
import re
import tempfile
import json
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values
import pandas as pd
from scholarly import scholarly
from psycopg2.extras import execute_values

# Parâmetros do pesquisador
pesquisador = ""
lattesId = ""
campus = ""

# Função para criar diretório temporário exclusivo para perfil Chrome
# Função para criar diretório temporário exclusivo do Chrome
def criar_diretorio_exclusivo():
    return tempfile.mkdtemp(prefix="chrome_profile_", dir="/tmp")


def extrair():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)



    driver.get("https://buscatextual.cnpq.br/buscatextual/busca.do?metodo=apresentar")
    sleep(5)

    driver.find_element(By.NAME, "buscarDemais").click()
    driver.find_element(By.NAME, "textoBusca").send_keys(pesquisador)
    driver.find_element(By.ID, "botaoBuscaFiltros").click()
    sleep(5)

    resultado_divs = driver.find_elements(By.CSS_SELECTOR, "div.resultado")
    if not resultado_divs:
        driver.quit()
        print("⚠️ Nenhum resultado encontrado")
        return

    pesquisadores = []
    for div in resultado_divs:
        pesquisadores.extend(div.find_elements(By.TAG_NAME, "li"))

    abriu_curriculo = False
    for li in pesquisadores:
        try:
            link = li.find_element(By.XPATH, ".//b/a")
            link.click()  # Abre o modal
            sleep(3)
            
            # Espera botão abrir currículo
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "idbtnabrircurriculo"))
            )
            
            driver.find_element(By.ID, "idbtnabrircurriculo").click()
            sleep(5)
            driver.switch_to.window(driver.window_handles[-1])  # Vai para a aba do currículo

            perfil = driver.find_element(By.CSS_SELECTOR, "div.infpessoa")
            if lattesId in perfil.text:
                abriu_curriculo = True
                break  # Achou o correto, sai do loop
            else:
                # Fecha a aba do currículo e retorna para a aba principal
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                # Fecha o modal do pesquisador errado
                driver.find_element(By.ID, 'idbtnfechar').click()
                sleep(2)

        except:
            continue

    if not abriu_curriculo:
        driver.quit()
        print("⚠️ Não consegui abrir currículo")
        return

    # Espera o conteúdo carregar
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.title-wrapper"))
        )
    except:
        print("⚠️ Conteúdo do currículo não carregou")
        driver.quit()
        return

    site = BeautifulSoup(driver.page_source, "html.parser")

    # Última atualização
    perfil_id = site.find("span", class_="img_cert icone-informacao-autor")
    if perfil_id:
        ultima_atualizacao = perfil_id.find_parent("li").text.strip()
        autores_atualizacao.append(pesquisador)
        atualizacao.append(ultima_atualizacao)
        print(pesquisador, "-", ultima_atualizacao)

    # === Projetos de Pesquisa ===
    target_div = site.find("a", {"name": "ProjetosPesquisa"})
    if target_div:
        target_div = target_div.find_parent("div", class_="title-wrapper")
        projetos_encontrados = target_div.find_all('div', class_='layout-cell layout-cell-3 text-align-right')
        padrao_ano = re.compile(r"\b(19\d{2}|20\d{2}|2100)\b")
        for pub in projetos_encontrados:
            anos_encontrados = pub.find_all("b", string=padrao_ano)
            if anos_encontrados:
                texto = pub.get_text(separator=" ", strip=True)
                autores_pesquisas.append(pesquisador)
                projetos_pesquisa.append(texto)
        print("Projetos de pesquisa encontrados" if projetos_pesquisa else "⚠️ Nenhum projeto encontrado")
    else:
        print("⚠️ A div 'Projetos de Pesquisa' não foi encontrada!")

    # === Produções Científicas ===
    target_div = site.find("a", {"name": "ProducoesCientificas"})
    if target_div:
        target_div = target_div.find_parent("div", class_="title-wrapper")
        categorias = target_div.find_all("div", class_="inst_back")
        for categoria in categorias:
            titulo_categoria = categoria.get_text(strip=True)
            elemento_atual = categoria.find_next_sibling()
            nome_subcategoria = ""
            while elemento_atual:
                if elemento_atual.name == "div" and "inst_back" in elemento_atual.get("class", []):
                    break
                if "cita-artigos" in elemento_atual.get("class", []):
                    subcat_b_tag = elemento_atual.find("b")
                    if subcat_b_tag:
                        nome_subcategoria = subcat_b_tag.get_text(strip=True, separator=" ")
                for pub in elemento_atual.find_all(class_="transform"):
                    texto_publicacao = pub.get_text(separator=" ", strip=True)
                    if texto_publicacao:
                        autores_publicacoes.append(pesquisador)
                        publicacoes.append(texto_publicacao)
                        categorias_publi.append(titulo_categoria)
                        subcategorias.append(nome_subcategoria)
                elemento_atual = elemento_atual.find_next_sibling()
        print("Produções científicas encontradas" if publicacoes else "⚠️ Nenhuma produção científica encontrada")
    else:
        print("⚠️ A div 'Produções Científicas' não foi encontrada!")

    # === Orientações ===
    target_div = site.find("a", {"name": "Orientacoes"})
    if target_div:
        target_div = target_div.find_parent("div", class_="title-wrapper")
        orientacoes_filtradas = target_div.find_all(['span', 'div', 'li'], class_='transform')
        for pub in orientacoes_filtradas:
            texto = pub.get_text(separator=" ", strip=True)
            if texto:
                autores_orientacoes.append(pesquisador)
                orientacoes.append(texto)
        print("Orientações encontradas" if orientacoes else "⚠️ Nenhuma orientação encontrada")
    else:
        print("⚠️ A div 'Orientações' não foi encontrada!")

    driver.close()
    #driver.switch_to.window(driver.window_handles[0])


# Inicializa listas
autores_publicacoes = []
publicacoes = []
categorias_publi = []
subcategorias = []

autores_orientacoes = []
orientacoes = []

autores_pesquisas = []
projetos_pesquisa = []

autores_atualizacao = []
atualizacao = []


DB_PARAMS = {
    "user": "ifdatalab_user",
    "password": "yui789&*(",
    "host": "10.26.1.73",
    "port": 5432,
    "dbname": "ifdatalab"
}


def table_exists(cur, table_name, schema="public") -> bool:
    cur.execute("""
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = %s
        AND table_name = %s
        LIMIT 1
    """, (schema, table_name))
    return cur.fetchone() is not None

def insert_df_with_cursor(cur, conn, df: pd.DataFrame, table: str):
    if df.empty:
        print(f"⚠️  {table}: DataFrame vazio, nada a inserir.")
        return
    if not table_exists(cur, table):
        print(f"🚫  {table}: tabela NÃO existe – nenhuma linha inserida.")
        return
    columns = [str(c) for c in df.columns]
    col_identifiers = sql.SQL(", ").join(map(sql.Identifier, columns))
    base_query = sql.SQL("INSERT INTO {} ({}) VALUES %s").format(
        sql.Identifier(table),
        col_identifiers
    )
    # Converte NaN para None
    values = [tuple(None if pd.isna(v) else v for v in row) for row in df.itertuples(index=False, name=None)]
    execute_values(cur, base_query.as_string(conn), values)
    print(f"✅  {table}: {len(df)} linhas inseridas.")


def upsert_ultima_atualizacao(cur, conn, tabela_upd: str, df_atualizacao: pd.DataFrame):
    if df_atualizacao.empty:
        return

    for _, row in df_atualizacao.iterrows():
        autor = row['autor']
        ultima_atualizacao = row['ultima_atualizacao']

        cur.execute("SELECT id FROM pesquisadores WHERE nome_completo = %s", (autor,))
        res = cur.fetchone()
        if not res:
            print(f"⚠️ Pesquisador '{autor}' não encontrado em 'pesquisadores'. Registro não inserido.")
            continue

        pesquisador_id = res[0]

        # Verifica se já existe registro na tabela
        cur.execute(
            sql.SQL("SELECT 1 FROM {} WHERE autor = %s").format(sql.Identifier(tabela_upd)),
            (autor,)
        )
        if cur.fetchone():
            cur.execute(
                sql.SQL("UPDATE {} SET ultima_atualizacao = %s WHERE autor = %s").format(sql.Identifier(tabela_upd)),
                (ultima_atualizacao, autor)
            )
        else:
            cur.execute(
                sql.SQL("INSERT INTO {} (autor, ultima_atualizacao, pesquisador_id) VALUES (%s, %s, %s)").format(sql.Identifier(tabela_upd)),
                (autor, ultima_atualizacao, pesquisador_id)
            )

    print(f"✅  {tabela_upd}: upsert manual concluído.")

def get_ids(cur, autor, campus_nome):
    cur.execute("SELECT id FROM campi WHERE nome_campus ILIKE %s", (campus_nome,))
    campus_row = cur.fetchone()
    if not campus_row:
        raise ValueError(f"Campus '{campus_nome}' não encontrado na tabela campi.")
    campus_id = campus_row[0]

    cur.execute("SELECT id FROM pesquisadores WHERE nome_completo = %s AND campus_id = %s", (autor, campus_id))
    pesquisador_row = cur.fetchone()
    if not pesquisador_row:
        raise ValueError(f"Pesquisador '{autor}' não encontrado para campus '{campus_nome}'.")
    pesquisador_id = pesquisador_row[0]

    return pesquisador_id, campus_id


def salvar_resultados_no_banco(df_publicacoes, df_orientacoes, df_projetos, df_producoes_gerais, df_atualizacao, campus_nome):
    params = DB_PARAMS.copy()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    try:
        # Adiciona pesquisador_id e campus_id em todos os DataFrames
        if not df_atualizacao.empty:
            autor = df_atualizacao.iloc[0]["autor"]
            pesquisador_id, campus_id = get_ids(cur, autor, campus_nome)

            for df in [df_publicacoes, df_orientacoes, df_projetos, df_producoes_gerais, df_atualizacao]:
                if not df.empty:
                    df["pesquisador_id"] = pesquisador_id
                    df["campus_id"] = campus_id

        # Insere cada dataframe nas respectivas tabelas
        insert_df_with_cursor(cur, conn, df_publicacoes, "publicacoes")
        insert_df_with_cursor(cur, conn, df_orientacoes, "orientacoes")
        insert_df_with_cursor(cur, conn, df_projetos, "projetos_pesquisa")
        insert_df_with_cursor(cur, conn, df_producoes_gerais, "producoes_gerais")

        # Upsert da última atualização em tabela específica por campus 
        tabela_upd = f"ultima_atualizacao_{campus_nome.lower()}"
        if table_exists(cur, tabela_upd):
            upsert_ultima_atualizacao(cur, conn, tabela_upd, df_atualizacao)
        else:
            print(f"ℹ️ Tabela {tabela_upd} não existe — pulando upsert.")

        conn.commit()
        print("✅ Commit realizado e conexão fechada.")
    except Exception as e:
        conn.rollback()
        print(f"Erro ao salvar no banco: {e}")
        raise
    finally:
        cur.close()
        conn.close()


def extrair_novo_pesquisador(nome, lattes_id, campus_nome):
    global pesquisador, lattesId, campus
    pesquisador = nome
    lattesId = lattes_id
    campus = campus_nome

    autores_publicacoes.clear(); publicacoes.clear(); categorias_publi.clear(); subcategorias.clear()
    autores_orientacoes.clear(); orientacoes.clear()
    autores_pesquisas.clear(); projetos_pesquisa.clear()
    autores_atualizacao.clear(); atualizacao.clear()

    # Roda a extração (preenche listas globais)
    extrair()

    # Constrói DataFrames com os resultados da extração
    df_publicacoes = pd.DataFrame({
        "autor":        autores_publicacoes,
        "publicacao":   publicacoes,
        "categoria":    categorias_publi,
        "subcategoria": subcategorias
    })

    df_orientacoes = pd.DataFrame({
        "autor":      autores_orientacoes,
        "orientacao": orientacoes
    })

    df_projetos = pd.DataFrame({
        "autor":            autores_pesquisas,
        "projeto_pesquisa": projetos_pesquisa
    })

    df_atualizacao = pd.DataFrame({
        "autor":              autores_atualizacao,
        "ultima_atualizacao": atualizacao
    })

    # Produções gerais
    producoes_tecnicas = df_publicacoes[df_publicacoes['categoria'] == "Produção técnica"][['publicacao', 'autor']]
    producoes_tecnicas_count = producoes_tecnicas.groupby('autor').size().reset_index(name='count')

    producoes_bibliograficas = df_publicacoes[df_publicacoes['categoria'] == "Produção bibliográfica"][['publicacao', 'autor']]
    producoes_bibliograficas_count = producoes_bibliograficas.groupby('autor').size().reset_index(name='count')

    orientacoes_count = df_orientacoes.groupby('autor').size().reset_index(name='count')
    projetos_count = df_projetos.groupby('autor').size().reset_index(name='count')

    df_producoes_gerais = df_atualizacao.merge(
        producoes_tecnicas_count.rename(columns={'count': 'producoes_tecnicas'}),
        on="autor", how="left"
    ).merge(
        producoes_bibliograficas_count.rename(columns={'count': 'producoes_bibliograficas'}),
        on="autor", how="left"
    ).merge(
        orientacoes_count.rename(columns={'count': 'orientacoes'}),
        on="autor", how="left"
    ).merge(
        projetos_count.rename(columns={'count': 'projetos_pesquisa'}),
        on="autor", how="left"
    )

    df_producoes_gerais.fillna(0, inplace=True)
    df_producoes_gerais = df_producoes_gerais.astype({
        "producoes_tecnicas": "int",
        "producoes_bibliograficas": "int",
        "orientacoes": "int",
        "projetos_pesquisa": "int"
    })

    salvar_resultados_no_banco(df_publicacoes, df_orientacoes, df_projetos, df_producoes_gerais, df_atualizacao, campus_nome)