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

        for token in ts:
            if token["label"].strip() != "":
                ts_validados.append(token)

        ts.clear()
        fita.extend(ts_validados)
        ts.extend(ts_validados)

    except FileNotFoundError:
        print("Erro ao abrir o arquivo './arquivos/codigo.txt'")
