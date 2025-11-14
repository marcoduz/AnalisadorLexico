from itertools import groupby
from src.analisador.lexico.afnd import AFND


def analisadorLexico(AFD: AFND, fita: list, ts: list, caminho_do_codigo: str):
    try:
        with open(caminho_do_codigo, "r") as arquivo:

            for i, linha in enumerate(arquivo):
                linhaFormatada = linha.strip()
                linhaSplit = linhaFormatada.split(" ")

                for label in linhaSplit:
                    estadoCorrente = AFD.estadoInicial

                    for c in label:
                        proximoEstado = AFD.proximoEstado(estadoCorrente, c)
                        if proximoEstado:
                            estadoCorrente = proximoEstado
                        else:
                            estadoCorrente = "X"
                            break

                    token_final = None

                    if estadoCorrente == "X":
                        token_final = "ERRO_LEXICO"
                    elif estadoCorrente in AFD.estadosFinais:
                        token_final = AFD.estadosFinais[estadoCorrente]
                    else:
                        token_final = "ERRO_LEXICO"
                        estadoCorrente = "X"

                    ts.append(
                        {
                            "linha": i + 1,
                            "token": token_final,
                            "label": label,
                            "estado_final": estadoCorrente,
                        }
                    )

        ts_validados = []
        ts.sort(key=lambda t: t["linha"])

        for linha, group in groupby(ts, key=lambda t: t["linha"]):
            tokens_da_linha = list(group)
            tem_erro = any(
                t["token"] == "ERRO_LEXICO" or t["estado_final"] == "X"
                for t in tokens_da_linha
            )

            if not tem_erro:
                # tokens_da_fita = [t["token"] for t in tokens_da_linha]
                fita.append(tokens_da_linha)
                ts_validados.extend(tokens_da_linha)

        ts.clear()
        ts.extend(ts_validados)

    except FileNotFoundError:
        print("Erro ao abrir o arquivo './arquivos/codigo.txt'")
