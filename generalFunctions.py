def calcularConjuntos(dados, limite = 10):
    from math import ceil
    conjuntos = []

    def somarSub(subElements):
        soma = 0
        for i in range(len(subElements)):
            soma += subElements[i]
        return soma

    def bruteForce():
        try:
            for z in range(ceil(len(dados)/2)):
                dadoZ = dados[-z-1]
                subconjunto = [dadoZ]
                subconjuntoindex = [len(dados)-z-1]
                if dadoZ == limite:
                    dados.remove(dadoZ)
                    conjuntos.append(dadoZ)
                    #print(dadoZ, flush=True)
                    bruteForce()
                output = bruteRecursion(subconjuntoindex, subconjunto)
                if  output == True: bruteForce()
                elif output == "exp1": break
                elif output == False: break
        except:
            pass
                        
    def bruteRecursion(subconjuntoindex, subconjunto):
        for i in range(len(dados)):
            if len(dados) < len(subconjuntoindex) and somarSub(subconjunto)+dados[i] != limite:
                return False

            if somarSub(subconjunto)+dados[i] == limite and i not in subconjuntoindex:
                subconjunto.append(dados[i])
                subconjuntoindex.append(i)
                conjuntos.append(subconjunto)

                for x in subconjunto:
                    dados.remove(x)
                return True#, print(subconjunto, subconjuntoindex, flush=True)
            elif somarSub(subconjunto)+dados[i] > limite and i not in subconjuntoindex:
                return "exp1"
            elif i not in subconjuntoindex:
                subconjunto.append(dados[i])
                subconjuntoindex.append(i)
                out = bruteRecursion(subconjuntoindex, subconjunto)
                if out ==  "exp1":
                    subconjunto.pop(-1)
                    subconjuntoindex.pop(-1)
                elif out == False:
                    subconjunto.remove(dados[i])
                    subconjuntoindex.remove(i)
                elif out == True: return True      
    
    def bruteForceFilter():
        #X Y Z. X limite -> Y+1. Y limite-> Z+1
        try:
            for z in range(len(dados)):
                dadoZ = dados[-z-1]
                subconjunto = [dadoZ]
                subconjuntoindex = [dados.index(dadoZ)]
                if dadoZ >= limite:
                    dados.remove(dadoZ)
                    conjuntos.append(dadoZ)
                    #print(dadoZ, flush=True)
                    bruteForceFilter()
                elif bruteRecursionFilter(subconjuntoindex, subconjunto):
                    bruteForceFilter()
                else:
                    break
        except:
            pass
                        
    def bruteRecursionFilter(subconjuntoindex, subconjunto):
        for i in range(len(dados)):
            if len(dados) < len(subconjuntoindex) and somarSub(subconjunto)+dados[i] != limite:
                return False

            
            if somarSub(subconjunto)+dados[i] >= limite and i not in subconjuntoindex:
                subconjunto.append(dados[i])
                subconjuntoindex.append(i)
                conjuntos.append(subconjunto)

                for x in subconjunto:
                    dados.remove(x)
                return True#, print(subconjunto, subconjuntoindex, flush=True)
            elif i not in subconjuntoindex:
                subconjunto.append(dados[i])
                subconjuntoindex.append(i)
                if not bruteRecursionFilter(subconjuntoindex, subconjunto):
                    subconjunto.remove(dados[i])
                    subconjuntoindex.remove(i)
                else: return True      
    
    bruteForce()
    #print("suboptmial", flush=True)
    bruteForceFilter()
    #print(dados,"===", flush=True)
    #print(conjuntos)
    return conjuntos, dados

def tratarDados(mensagem, bot, message):
    final = []
    limite = 10
    bonus = 0
    print(final)
    print(mensagem)
    for i in range(len(mensagem)):
        try: 
            if int(mensagem[i]) < 0: mensagem[i] = int(mensagem[i])*-1
            final.append(int(mensagem[i])) 
        except:
            try: 
                limite = int(mensagem[i].removeprefix("/"))
                if limite < 0: limite = limite*-1
            except: 
                try:
                    print('sheeesh')
                    bonus = int(mensagem[i].removeprefix("*")) 
                except: bot.send_message(message.chat.id, f'valor "{mensagem[i]}" foi desconsiderado')
    
    
    if bonus != 0:
        for i in range(len(final)):
            final[i] = final[i] + bonus
    final.sort()
    return final, limite

def tratarResposta(operacao, conjuntos, dadosRestantes, bot, message):
    operacao.sort()
    mensagemOperacao = ''
    mensagemConjunto = ''
    mensagemRestantes = ''
    print('oper', operacao)
    print('conj', conjuntos)
    print('resto', dadosRestantes)
    for i in range(len(operacao)):
        if i > 0:
            mensagemOperacao = mensagemOperacao + f', {operacao[i]}'
        else:
            mensagemOperacao = mensagemOperacao + f' {operacao[i]}'
    for i in range(len(conjuntos)):
        try:
            for a in range(len(conjuntos[i])):
                if a > 0:
                    mensagemConjunto = mensagemConjunto + f', {conjuntos[i][a]}'
                else:
                    mensagemConjunto = mensagemConjunto + f'{conjuntos[i][a]}'
        except: 
            if i > 0:
                mensagemConjunto = mensagemConjunto + f', {conjuntos[i]}'
            else:
                mensagemConjunto = mensagemConjunto + f'{conjuntos[i]}'
        finally:
            if i != len(conjuntos)-1: mensagemConjunto = mensagemConjunto + " | "

    for i in range(len(dadosRestantes)):
        if i > 0:
            mensagemRestantes = mensagemRestantes + f', {dadosRestantes[i]}'
        else:
            mensagemRestantes = mensagemRestantes + f' {dadosRestantes[i]}'
    bot.send_message(message.chat.id, f'''
    <b>Suas rolagens🎲</b>
    <b>Pool inicial:</b> {mensagemOperacao}
    <b>Apostas: {len(conjuntos)}</b> <i>({mensagemConjunto})</i>
    <b>Dados Traidores:</b> {len(dadosRestantes)} <i>({mensagemRestantes})</i>''', parse_mode='HTML')

'''
mensagem = ['5', '4', '3', '6', '7']
for i in range(len(mensagem)):

    if mensagem[i] < 0: mensagem[i] = mensagem[i]*-1
    print[mensagem, i]

    print(int(mensagem[i]))



######DEBUG#######
# 1,1,2,2,2,2,5,5
# 1,2,3,4,5,6,7,8,9,10
#1,1,1,1,1,7,8
# 2, 3, 4, 4, 5, 5, 5, 6, 8, 9
# 1,3,5,5,5,5,5,8

calcularConjuntos([1,1,2,2,2,2,5,5])

for i in range(1):
    x = 10
    conjunto = []
    for a in range(x):
        conjunto.append(randint(1,10))
    try:
        conjunto.sort()
        print(conjunto, flush=True)
        calcularConjuntos(conjunto, 10)
    except:
        print("FALHOU", conjunto, flush=True)
        break'''

'''
Parte de imagens!!!
'''

def catalogo():
    import os
    from PIL import Image
    from io import BytesIO

    #response = requests.get(url)
    #img = Image.open(BytesIO(response.content))

    info = []
    for root, __, files in os.walk("https://drive.google.com/drive/u/0/folders/16qbFc7c-IFkYPTb8Q6xGekmzhQGFAgl3"):
        for f in files:
            if f.endswith(".jpg"):
                info.append(Image.open(os.path.join(root, f)))#{f"img{f}":'''
    return info


print('rodando...')