def analisadorLexico(AFD, fita, ts):
    try:
        with open('./arquivos/codigo.txt', 'r') as arquivo:
            print('lendo o arquivo')
            for i, linha in enumerate(arquivo):
                linhaFormatada = linha.strip() ##Remove o \n da quebra de linha
                linhaSplit = linhaFormatada.split(' ')

                for label in linhaSplit:
                    estadoCorrente = AFD.estadoInicial
                    for c in label:
                        proximoEstado = AFD.proximoEstado(estadoCorrente, c)
                        if(proximoEstado):
                            estadoCorrente = proximoEstado
                        else:
                            estadoCorrente = 'X'
                            break
                    if(not (estadoCorrente in AFD.estadosFinais)):
                        estadoCorrente = 'X'
                    fita.append(estadoCorrente)
                    ts.append({'linha': i, 'estado': estadoCorrente, 'label': label})
            pass
    except FileNotFoundError:
        print("Erro ao abrir o arquivo")