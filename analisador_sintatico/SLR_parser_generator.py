from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from gramatica_livre_contexto.GLC import GLC


def obter_dados_completos_do_site(
    gramatica_em_texto: str, dados_extraidos: dict[str, list[str]] = None
):
    """
    Abre uma janela do Chrome, insere a gramática, e extrai:
    1. A tabela de FIRST e FOLLOW.
    2. A tabela de parsing SLR.
    Retorna um dicionário com todos os dados.
    """
    print("Iniciando automação do navegador...")

    driver = webdriver.Chrome()

    try:
        url = "https://jsmachines.sourceforge.net/machines/slr.html"
        driver.get(url)
        print("Página aberta com sucesso.")

        # --- 1. INSERIR A GRAMÁTICA ---
        textarea = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "grammar"))
        )
        textarea.clear()
        textarea.send_keys(gramatica_em_texto)
        print("Gramática inserida.")

        # --- 2. GERAR AS TABELAS ---
        botao_gerar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@type='button' and @value='>>']")
            )
        )
        botao_gerar.click()
        print("Botão clicado!")

        # --- 3. PEGAR A TABELA DE FIRST E FOLLOW ---
        tabela_ff_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "firstFollowView"))
        )
        linhas_ff = tabela_ff_div.find_elements(By.TAG_NAME, "tr")
        for linha in linhas_ff:
            celulas = linha.find_elements(By.XPATH, ".//th | .//td")
            linha_dados = [celula.text.replace("\n", "") for celula in celulas]
            if linha_dados:
                dados_extraidos["first_follow"].append(linha_dados)
        print("Tabela de FIRST e FOLLOW extraída com sucesso!")

        # --- 4. PEGAR A TABELA DE PARSING SLR ---
        tabela_slr_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "lrTableView"))
        )
        linhas_slr = tabela_slr_div.find_elements(By.TAG_NAME, "tr")
        for linha in linhas_slr:
            celulas = linha.find_elements(By.XPATH, ".//th | .//td")
            linha_dados = [celula.text.replace("\n", "").strip() for celula in celulas]
            if linha_dados and "LR table" not in linha_dados[0]:
                dados_extraidos["tabela_slr"].append(linha_dados)
        print("Tabela de parsing SLR extraída com sucesso!")

        return

    except Exception as e:
        print("\n--- OCORREU UM ERRO ---")
        print("A automação falhou. Verifique a janela do navegador.")
        print(f"Erro do Selenium: {e.args}")

        print("\nDeixando o navegador aberto por 30 segundos para inspeção final...")
        time.sleep(30)

        return None
    finally:
        print("Fechando o navegador.")
        driver.quit()
        


def gerar_gramatica(glc: GLC) -> str | None:
    print("\nFormatando a gramática para o formato de texto...")

    simbolo_inicial = (
        glc.simbolo_inicial if glc.simbolo_inicial else glc.naoTerminais[0]
    )

    regras_texto = []

    regras_texto.append(f"S' -> {simbolo_inicial}")

    for nao_terminal, producoes in glc.gramatica.items():

        for producao in producoes:
            regra = f"{nao_terminal} -> {producao.replace('ε', "''")}"
            #print(regra)
            regras_texto.append(regra)

    gramatica_final_texto = "\n".join(regras_texto)

    dados = {
        "producoes": [],
        "first_follow": [],
        "tabela_slr": [],
    }

    for index, regra in enumerate(regras_texto, 0):
        dados["producoes"].append([index, regra])

    obter_dados_completos_do_site(gramatica_final_texto, dados)

    if dados:
        # print("\n--- Tabela de FIRST e FOLLOW ---\n")
        # for linha in dados["first_follow"]:
        #     print(linha)

        # print("\n--- Tabela de Parsing SLR ---\n")
        # for linha in dados["tabela_slr"]:
        #     print(linha)

        return dados

    return None
