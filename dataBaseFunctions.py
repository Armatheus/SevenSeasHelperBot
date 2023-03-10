from tinydb import TinyDB, Query
from tinydb.operations import *

imgdb = TinyDB('7thSeaImgDb.json')
imagens = Query()
class ImageDataBase():
    def adicionarImagem(self, tag, url):
        if imgdb.search(imagens.tag == tag) == [] and imgdb.search(imagens.url == url) == []:
            imgdb.insert({'tag': tag, 'url': url})
            return True
        else:
            return False

    def deletarImagem(self, tag):
        if tag:
            imgdb.remove(imagens.tag == tag)
            return True
        else:
            return False

    def catalogo(self):
        listaTags = []
        listaUrls = []
        for i in range(len(imgdb)):
            listaTags.append(imgdb.all()[i]['tag'])
            listaUrls.append(imgdb.all()[i]['url'])
        return listaTags, listaUrls

    def encontrarImagem(self, tag):
        try:
            resultado = imgdb.search(imagens.tag == tag)
            #print(resultado, '=== resultado')
            return resultado[0]['url']
        except: return False

    def renomearTag(self, tag, newTag):
        try:
            lista = imgdb.update({'tag': newTag}, imagens.tag == tag)
            if lista == []:
                return False
            return True
        except: return False

#imgdb.truncate()
#print(imgdb.all())

pjdb = TinyDB('PJsSheetDb.json')
jogador = Query()
class Jogador():
    #||------------------------||
    #||    SETUP DA DATABASE   ||
    #||------------------------||
    def __init__(self) -> None:
        self.mestreID = [1486739015]

    def criarFicha(self, message):
        jogadorID = message.from_user.id
        jogadorNome = message.from_user.username
        cargo = 'jogador'
        chatID = message.chat.id
        if jogadorID == 1486739015:
            cargo = 'mestre'
        
        phInicial = 1
        fortunaInicial = 0
        if pjdb.count(jogador.rg.jogadorID == jogadorID) == 0:
            id = pjdb.insert({
                'rg': {'jogadorID': jogadorID, 
                    'jogadorNome': jogadorNome, 
                    'cargo': cargo},
                'chatID': chatID,
                'iniciais': {'ph': phInicial, 'fortuna': fortunaInicial},
                'status': {'ph': phInicial, 'fortuna': fortunaInicial}
                })
            IDs = pjdb.get(jogador.IDs.exists())
            #x = pjdb.all()[1]['IDs']
            y = pjdb.get(jogador.IDs.exists())['IDs']
            y.append(id)
            pjdb.update({'IDs': y}, doc_ids=[IDs.doc_id])
    
    #||------------------------||
    #||      FUNÇÕES GET       ||
    #||------------------------||
    def getIDs(self):
        return pjdb.get(jogador.IDs.exists())['IDs']
    
    def getPlayerID(self, nome):
        ficha = pjdb.get(jogador.rg.jogadorNome == nome)
        return ficha['chatID']

    def getAllNames(self):
        nomes = []
        for id in self.getIDs():
            ficha = pjdb.get(doc_id=id)
            nomes.append(ficha['rg']['jogadorNome'])
        return nomes

    def getFichasCriadas(self):
        fichasCriadasLista = []
        for id in self.getIDs():
            ficha = pjdb.get(doc_id=id)
            fichasCriadasLista.append(ficha['chatID'])
        return fichasCriadasLista

    #||------------------------||
    #||    FUNC DE CONSULTA    ||
    #||------------------------||
    def consultarJogadores(self, call):
        if call.from_user.id in self.mestreID:
            mensagem = ''
            for id in self.getIDs():
                ficha = pjdb.get(doc_id=id)
                mensagem = mensagem + f'''
<b>Jogador:</b> {ficha['rg']['jogadorNome']}
  <b>PH:</b> {ficha['status']['ph']}
  <b>Fortuna</b> {ficha['status']['fortuna']}
'''
        else: 'você não tem permissão para ver os dados de todos os jogadores'
        return mensagem

    def consultarFicha(self, id):
        ficha = pjdb.get(jogador.chatID == id)['status']

        mensagem = f'''
        <b>Sua ficha</b>
        <b>Pontos Heroicos:</b> {ficha['ph']}
        <b>Fortuna:</b> {ficha['fortuna']}'''
        return mensagem

    #||------------------------||
    #||    EDIÇÃO DE FICHAS    ||
    #||------------------------||
    def adicionarPH(self, id, n):
        ficha = pjdb.get(jogador.chatID == id)
        phAntigo = ficha['status']['ph']
        #phInicial = ficha['ph']['inicial']
        phNovo = ficha['status']['ph'] + n

        pjdb.update({'status': {'ph': phNovo, 'fortuna': ficha['status']['fortuna']}}, doc_ids=[ficha.doc_id])

        return [phAntigo, phNovo]

    def adicionarFortuna(self, id, n):
        ficha = pjdb.get(jogador.chatID == id)
        fortunaAntiga = ficha['status']['fortuna']
        #fortunaInicial = ficha['fortuna']['inicial']
        fortunaNova = ficha['status']['fortuna'] + n
        pjdb.update({'status': {'ph': ficha['status']['ph'], 'fortuna': fortunaNova}}, doc_ids=[ficha.doc_id])
        return fortunaAntiga, fortunaNova

    def resetPJ(self, atributo, nome):
        mensagem = ' '
        print(nome, '================')
        for name in nome:
            try:
                ficha = pjdb.get(jogador.rg.jogadorNome == name)

                if atributo == 'ph':
                    pjdb.update({'status':{'ph': ficha['iniciais']['ph'], 'fortuna': ficha['status']['fortuna']}}, doc_ids=[ficha.doc_id])
                    mensagem = mensagem + f'''
<b>{name}</b>'''+ self.consultarFicha(ficha['chatID'])
                    print('mensagem loop',name,mensagem)
                elif atributo == 'fortuna':
                    pjdb.update({'status':{'ph': ficha['status']['ph'], 'fortuna': ficha['iniciais']['fortuna']}}, doc_ids=[ficha.doc_id])
                    mensagem = mensagem + f'''
<b>{name}</b>'''+ self.consultarFicha(ficha['chatID'])
                elif atributo == 'all':
                    pjdb.update({'status':{'ph': ficha['iniciais']['ph'], 'fortuna': ficha['iniciais']['fortuna']}}, doc_ids=[ficha.doc_id])
                    mensagem = mensagem + f'''
<b>{name}</b>'''+ self.consultarFicha(ficha['chatID'])
            except: mensagem = mensagem + f'''
        comando falho para {name}'''
        print('mensagem:', mensagem)
        return mensagem 
            
    def give(self, nomes, atributo, quantia):
        for nome in nomes:
            ficha = pjdb.get(jogador.rg.jogadorNome == nome)
            if atributo == 'ph':
                #phInicial = ficha['ph']['inicial']
                Novo = ficha['status']['ph'] + int(quantia)

                pjdb.update({'status': {'ph': Novo, 'fortuna': ficha['status']['fortuna']}}, doc_ids=[ficha.doc_id])
                #return f'O mestre te enviou {quantia} Pontos Heróicos!'
            elif atributo == 'fortuna':
                #phInicial = ficha['ph']['inicial']
                Novo = ficha['status']['fortuna'] + quantia

                pjdb.update({'status': {'ph': ficha['status']['ph'], 'fortuna': Novo}}, doc_ids=[ficha.doc_id])
                #return f'O mestre te enviou {quantia} pontos de Fortuna!'


    #||------------------------||
    #||     ÁREA DO MESTRE     ||
    #||------------------------||
    def adicionarMestre(self, message, id):
        if message.chat.id in self.mestreID:
            self.mestreID.append(id)
        else: return 'você não tem permissão para esta ação'
    
    def retirarMestre(self, message, id):
        if message.chat.id in self.mestreID:
            self.mestreID.remove(id)
        else: return 'você não tem permissão para esta ação'


    #===========
