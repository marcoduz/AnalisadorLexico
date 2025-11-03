from itertools import groupby
from automato.AFND import AFND


def analisadorLexico(AFD: AFND, fita: list, ts: list):
    try:
        with open("./arquivos/codigo.txt", "r") as arquivo:

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

                    if estadoCorrente in AFD.estadosFinais:
                        token_final = AFD.estadosFinais[estadoCorrente]

                    if not (estadoCorrente in AFD.estadosFinais):
                        estadoCorrente = "X"
                        token_final = "ERRO_LEXICO"

                    ts.append(
                        {
                            "linha": i + 1,
                            "token": token_final,
                            "label": label,
                            "estado_final": estadoCorrente,
                        }
                    )

        for _, group in groupby(ts, key=lambda t: t["linha"]):
            tokens_da_linha = list(group)
            tem_erro = any(t["token"] == "ERRO_LEXICO" for t in tokens_da_linha)

            if not tem_erro:
                fita_da_linha = " ".join([t["token"] for t in tokens_da_linha])
                fita.append(fita_da_linha)

    except FileNotFoundError:
        print("Erro ao abrir o arquivo './arquivos/codigo.txt'")
