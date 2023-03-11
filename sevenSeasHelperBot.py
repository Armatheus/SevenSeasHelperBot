import os
from random import randint

import telebot
from dataBaseFunctions import *
from generalFunctions import *
from turnFunctions import *
from dotenv import load_dotenv
from telebot.handler_backends import ContinueHandling
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

API_KEY = os.getenv('API_KEY_SEVENSEAS')
bot = telebot.TeleBot(API_KEY)
#bot.edit_message_text(chat_id=CHAT_WITH_MESSAGE, text=NEW_TEXT, message_id=MESSAGE_TO_EDIT)

#||------------------------||
#||         Markup         ||
#||------------------------||
def markup_jogador():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Adicionar PH ⭐️', callback_data='cb_ph'),
               InlineKeyboardButton('Adicionar Fortuna 💰', callback_data='cb_fortuna'),
               InlineKeyboardButton('🚧Adicionar Aposta🚧', callback_data='cb_aposta'),
               InlineKeyboardButton('🚧Ordem de Iniciativa🚧', callback_data='cb_iniciativa'),
               InlineKeyboardButton('Ficha 📰', callback_data='cb_ficha')
               )
    return markup
def markup_mestre():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Resetar PJs ♻️', callback_data='cb_reset'),
               InlineKeyboardButton('Dar PH e Fortuna 🎁', callback_data='cb_give'),
               InlineKeyboardButton('Iniciativa 📜', callback_data='cb_markupIniciativa'),
               InlineKeyboardButton('Jogadores 🏴‍☠️', callback_data='cb_jogadores'),
               )
    return markup
def markup_iniciativa():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Nova Iniciativa ♻️', callback_data='cb_iniciarIniciativa'),
               InlineKeyboardButton('Adicionar NPC 🏴‍☠️', callback_data='cb_adicionarNPC'),
               InlineKeyboardButton('Adicionar Apostas 🔥', callback_data='cb_apostasMestre'),
               InlineKeyboardButton('Ver Iniciativa 📜', callback_data='cb_iniciativaMestre'),
               InlineKeyboardButton('Voltar 🔙', callback_data='cb_voltar'),
               )
    return markup

def player_list_markup():
    listaPlayers = playerHandler.getAllNames()
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for nome in listaPlayers:
        markup.add(InlineKeyboardButton(nome, callback_data=nome))
    markup.add(InlineKeyboardButton('Todos', callback_data='cb_allPlayers'),
               InlineKeyboardButton('Fim', callback_data='cb_fim'))
    return markup
def player_givelist_markup():
    listaPlayers = playerHandler.getAllNames()
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for nome in listaPlayers:
        markup.add(InlineKeyboardButton(nome, callback_data=nome))
    markup.add(InlineKeyboardButton('Todos', callback_data='cb_giveAllPlayers'),
               InlineKeyboardButton('Fim', callback_data='cb_giveFim'))
    return markup
def player_inlist_markup():
    listaPlayers = playerHandler.getAllNames()
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for nome in listaPlayers:
        markup.add(InlineKeyboardButton(nome, callback_data=nome))
    markup.add(InlineKeyboardButton('Todos', callback_data='cb_inAllPlayers'),
               InlineKeyboardButton('Fim', callback_data='cb_inFim'))
    return markup
def player_apostalist_markup():
    listaPlayers = computarIniciativa()
    print(listaPlayers)
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for player in listaPlayers:
        nome = player['nome']
        markup.add(InlineKeyboardButton(nome, callback_data=f'{nome}_aposta'))
    return markup

def reset_markup():
    pass
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Pontos Heróicos ⭐️', callback_data='cb_resetPH'),
               InlineKeyboardButton('Fortuna 💰', callback_data='cb_resetFortuna'),
               InlineKeyboardButton('Tudo', callback_data='cb_resetAll')
               )
    return markup
def give_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('PH ⭐️', callback_data='cb_givePH'),
               InlineKeyboardButton('Fortuna 💰', callback_data='cb_giveFortuna')
               )
    return markup
'''def player_list_markup():
    listaPlayers = playerHandler.getAllNames()
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for nome in listaPlayers:
        markup.add(InlineKeyboardButton(nome, callback_data=nome))
    markup.add(InlineKeyboardButton('Todos', callback_data='cb_allPlayers'),
               InlineKeyboardButton('Fim', callback_data='cb_fim'))
    return markup'''
#Handlers & Funções Gerais
imageHandler = ImageDataBase()
playerHandler = Jogador()

#||------------------------||
#||       Funções          ||
#||------------------------||
def enviarMensagem(nome, texto):
    playerID = playerHandler.getPlayerID(nome)
    bot.send_message(playerID, texto)

#||------------------------||
#||         HELP           ||
#||------------------------||
@bot.message_handler(commands=['help'])
def greet(message): 

    bot.reply_to(message, '''
Funções do bot:
<b>☆Agrupar dados em apostas☆</b>

-Mande um conjunto de números <u>separados por um espaço</u>, 
<i>ex: "1 1 9 8 7". Números negativos viram positivos, e letras são desconsideradas</i>.
-Se quiser <u>mudar o limite</u> coloque um <u>"/X"</u> na mensagem, 
<i>ex: "5 5 5 /15", o limite padrão é 10</i>.
-Caso queira <u>adicionar um bônus</u> em todos os dados rolados, coloque um <u>"*X"</u> na mensagem, <i>por exemplo: "1 3 5 4 10 *2" -> "3 5 7 6 12"</i>.
<i>A ordem dos fatores não altera o produto, <b>mas o primeiro número não pode conter letras, "/" ou "*"</b> </i>


<b>☆Controlar sua Ficha☆</b>

mande um "/f" no chat, é bem intuitivo.
    ''', parse_mode='HTML')

#||------------------------||
#||    ÁREA DE IMAGENS     ||
#||------------------------||
@bot.message_handler(commands=['imagem'])
def greet(message):     
    print(message.chat.username, message.text, 'imagem')
    mensagem = message.text
    mensagem = mensagem.split(' ')
    operacao = mensagem[1]
    operacao = operacao.lower()

    if operacao == 'nova' or operacao== 'adicionar':
        try:
            resultado = imageHandler.adicionarImagem(mensagem[2], mensagem[3])
            if resultado:
                print(mensagem[3])
                bot.send_message(message.chat.id, 'Imagem adicionada')
                try: bot.send_photo(message.chat.id, 'https://docs.google.com/uc?id='+ mensagem[3])
                except: bot.send_message(message.chat.id, 'mas a imagem é incompativel, delete ela antes de continuar')
            elif not resultado:
                bot.send_message(message.chat.id, 'essa imagem já existe')
        except:
            bot.send_message(message.chat.id, 'ERROR 001, verifique se colocou "tag url"')
    elif operacao == 'deletar':
        try:
            resultado = imageHandler.deletarImagem(mensagem[2])
            if resultado:
                bot.send_message(message.chat.id, 'imagem deletada >:3')
            elif not resultado:
                bot.send_message(message.chat.id, 'imagem não encontrada')
        except:
            bot.send_message(message.chat.id, 'ERROR 002')
    elif operacao == 'catalogo'or operacao=='galeria':
        try:
            listas = imageHandler.catalogo()
            bot.send_message(message.chat.id, 'seu catálogo:')
            for i in range(len(listas[0])):
                try:
                    bot.send_photo(message.chat.id, 'https://docs.google.com/uc?id='+listas[1][i], caption=f'{listas[0][i]}')
                except:
                    bot.send_message(message.chat.id, f'a imagem {listas[0][i]} não pode ser carregada.')
        except: bot.send_message(message.chat.id, 'ERROR 005')
    elif operacao == 'help':
        try:
            bot.send_message(message.chat.id, '''
    O comando de imagem é apenas para o mestre, por favor não mude nada, as mudanças são feitas num database, então é irreversível

    <b>nova (ou adicionar):</b> tag, url cortada 
    <b>deletar:</b> tag
    <b>catalogo(ou galeria):</b> nada
    <b>renomear:</b> tag, nova tag
        ''', 'HTML')
        except: bot.send_message(message.chat.id, 'ERROR 006, mermão, o help deu error, fodeu')
    elif operacao == 'renomear':
        '''try:'''
        rename = imageHandler.renomearTag(mensagem[2], mensagem[3])
        if rename:
            bot.send_message(message.chat.id, 'renomeado com sucesso')
        elif not rename:
            bot.send_message(message.chat.id, 'não foi possível mudar a tag')
        '''except:
            bot.send_message(message.chat.id, 'ERROR 003')'''
    else: 
        try:
            find = imageHandler.encontrarImagem(mensagem[1])
            if not find:
                bot.send_message(message.chat.id, 'imagem não encontrada')
            else:
                bot.send_photo(message.chat.id, 'https://docs.google.com/uc?id='+find, caption=f'{mensagem[1]}')
        except: bot.send_message(message.chat.id, 'ERROR 004')
    pass

#------------------------
#    CALL BACK MANAGER
#------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_player(call):
    def quantidadeStr():
        txt = ''
        for i in range(len(callback_player.quantidade)):
            txt = txt + str(callback_player.quantidade[i])
        return txt
        
    if call.data == 'cb_ficha':
        ficha = playerHandler.consultarFicha(call.from_user.id)
        bot.send_message(call.from_user.id, ficha, 'HTML', reply_markup=markup_jogador())
    elif call.data == 'cb_ph':
        msg = bot.send_message(call.from_user.id, 'Quantos pontos quer adicionar? (números negativos são aceitos)')
        bot.register_next_step_handler(msg, atualizarPH)
    elif call.data == 'cb_fortuna':
        msg = bot.send_message(call.from_user.id, 'Quantos pontos quer adicionar? (números negativos são aceitos)')
        bot.register_next_step_handler(msg, atualizarFortuna)
    elif call.data == 'cb_aposta' or call.data == 'cb_iniciativa': bot.send_message(call.from_user.id, '''Função ainda não disponível 
┐(‘～`；)┌''', reply_markup=markup_jogador())

    else:         
        ##TECLADO NUMERICO
        for i in range(3):
            if call.data == f'num_{(i*3)+1}':
                callback_player.quantidade.append((i*3)+1)
                quantidadeStr = quantidadeStr()
                bot.edit_message_text(chat_id=call.from_user.id, text=quantidadeStr, message_id=callback_player.mensagemID)
        if call.data == 'num_0':
            callback_player.quantidade.append(0)
            quantidadeStr = quantidadeStr()
            bot.edit_message_text(chat_id=call.from_user.id, text=quantidadeStr, message_id=callback_player.mensagemID)
        elif call.data == 'num_apagar':
            callback_player.quantidade.pop()
            quantidadeStr = quantidadeStr()
            bot.edit_message_text(chat_id=call.from_user.id, text=quantidadeStr, message_id=callback_player.mensagemID)
        return ContinueHandling()

#------------------------
#    Funções de ficha  
#------------------------

def atualizarPH(message):
    quantia = message.text
    try: quantia = int(quantia)
    except:
        quantia.lower()
        if quantia != 'cancelar': 
            msg = bot.send_message(message.from_user.id, 'Por favor, envie um número inteiro, envie "cancelar" para cancelar a operação')
            bot.register_next_step_handler(msg, atualizarPH)
        return
    data = playerHandler.adicionarPH(message.from_user.id, quantia)
    return bot.send_message(message.from_user.id, f'<b>Pontos Heroicos:</b> {data[0]} → {data[1]}', 'HTML', reply_markup=markup_jogador())
def atualizarFortuna(message):
    quantia = message.text
    try: quantia = int(quantia)
    except:
        quantia.lower()
        if quantia != 'cancelar': 
            msg = bot.send_message(message.from_user.id, 'Por favor, envie um número inteiro, envie "cancelar" para cancelar a operação')
            bot.register_next_step_handler(msg, atualizarFortuna)
        return
    data = playerHandler.adicionarFortuna(message.from_user.id, quantia)
    return bot.send_message(message.from_user.id, f'<b>Fortuna:</b> {data[0]} → {data[1]}', 'HTML', reply_markup=markup_jogador())
    
#||------------------------||
#||      ÁREA DA FICHA     ||
#||------------------------||
@bot.message_handler(commands=['f'])
def wellcome(message):
    jogadores = playerHandler.getFichasCriadas()
    if message.chat.id in jogadores: 
        bot.send_message(message.chat.id, 'Bem-vinda/Bem-vindo à area de ficha do bot! O que deseja fazer?', reply_markup=markup_jogador())
    else:
        playerHandler.criarFicha(message)
        bot.send_message(message.chat.id, 'Sua ficha foi criada, e agora?', reply_markup=markup_jogador())

#||------------------------||
#||     ÁREA DO MESTRE     ||
#||------------------------||
@bot.message_handler(commands=['m'])
def wellcome(message):
    if  message.chat.id in playerHandler.mestreID:
        bot.send_message(message.chat.id, 'Qual o comando?', reply_markup=markup_mestre())
    else:
        bot.send_message(message.chat.id, '''Você não tem permissão para acessar os comandos de mestre
┐(‘～`；)┌''')

#------------------------
#    CALL BACK MANAGER
#------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_mestre(call):
    print(computarIniciativa())

    if call.data == 'cb_reset':
        callback_mestre.listaJogadores = []
        bot.send_message(call.from_user.id, 'Quais jogadores deseja resetar? ("all" para todos)', reply_markup=player_list_markup())
        #bot.register_next_step_handler(msg, resetHandler)
    elif  call.data == 'cb_give':
        callback_mestre.listaJogadores = []   
        bot.send_message(call.from_user.id, 'Quais jogadores deseja resetar? ("all" para todos)', reply_markup=player_givelist_markup())
    elif  call.data == 'cb_jogadores':
        message = playerHandler.consultarJogadores(call)
        bot.send_message(call.from_user.id, message, 'HTML', reply_markup=markup_mestre())
    elif call.data == 'cb_iniciarIniciativa':
        callback_mestre.listaJogadores = [] 
        bot.send_message(call.from_user.id, 'Quais jogadores estarão na cena?', reply_markup=player_inlist_markup())
    elif call.data == 'cb_adicionarNPC':
        msg = bot.send_message(call.from_user.id, 'Qual o nome do NPC?')
        bot.register_next_step_handler(msg, registrarNPC)
    elif call.data == 'cb_markupIniciativa':
        msg = bot.send_message(call.from_user.id, 'Menu de Iniciativa', reply_markup=markup_iniciativa())
    elif call.data == 'cb_voltar':
        msg = bot.send_message(call.from_user.id, 'Voltando...', reply_markup=markup_mestre())
    elif call.data == 'cb_iniciativaMestre':
        bot.send_message(call.from_user.id, 'Iniciativa: \n'+apresentarIniciativa(), reply_markup=markup_iniciativa())
    elif call.data == 'cb_apostasMestre':
        msg = bot.send_message(call.from_user.id, 'Qual personagem mudar?', reply_markup=player_apostalist_markup())
    #SELECIONANDO ATRIBUTO DO RESET
    elif call.data == 'cb_resetPH':
        print('LISTAJOGADORES:',callback_mestre.listaJogadores)
        txt = playerHandler.resetPJ('ph', callback_mestre.listaJogadores)
        bot.send_message(call.from_user.id, txt, 'HTML', reply_markup=markup_mestre())
    elif call.data == 'cb_resetAll': 
        print('LISTAJOGADORES:',callback_mestre.listaJogadores)
        txt = playerHandler.resetPJ('all', callback_mestre.listaJogadores)
        bot.send_message(call.from_user.id, txt, 'HTML', reply_markup=markup_mestre())
    elif call.data == 'cb_resetFortuna': 
        print('LISTAJOGADORES:',callback_mestre.listaJogadores)
        txt = playerHandler.resetPJ('fortuna', callback_mestre.listaJogadores)
        bot.send_message(call.from_user.id, txt, 'HTML', reply_markup=markup_mestre())
    #SELECIONANDO JOGADORES DO RESET
    elif call.data in playerHandler.getAllNames():
        callback_mestre.listaJogadores.append(call.data)
        bot.send_message(call.from_user.id, call.data+' adicionado')
    elif call.data == 'cb_fim':
        bot.send_message(call.from_user.id, 'Quais atributos mudar?', reply_markup=reset_markup())
    elif call.data == 'cb_allPlayers':
        callback_mestre.listaJogadores = playerHandler.getAllNames()
        bot.send_message(call.from_user.id, 'Todos os jogadores foram adicionados')
    
    #SELECIONANDO JOGADORES DO GIVE
    elif call.data == 'cb_giveFim':
        bot.send_message(call.from_user.id, 'Qual atributo mudar?', reply_markup=give_markup())
    elif call.data == 'cb_giveAllPlayers':
        callback_mestre.listaJogadores = playerHandler.getAllNames()
        bot.send_message(call.from_user.id, 'Todos os jogadores foram adicionados')
    #SELECIONANDO O ATRIBUTO DO GIVE
    elif call.data == 'cb_givePH':
        msg = bot.send_message(call.from_user.id, 'Quantos pontos quer adicionar? (números negativos são aceitos)')
        bot.register_next_step_handler(msg, givePH)
    elif call.data == 'cb_giveFortuna':
        msg = bot.send_message(call.from_user.id, 'Quantos pontos quer adicionar? (números negativos são aceitos)')
        bot.register_next_step_handler(msg, giveFortuna)
    
    #CRIANDO UMA NOVA INICIATIVA
    elif call.data == 'cb_inFim':
        #bot.send_message(call.from_user.id, 'Qual atributo mudar?', reply_markup=give_markup())
        txt = abrirIniciativa(callback_mestre.listaJogadores)
        bot.send_message(call.from_user.id, f'Jogadores em cena: \n{txt}', reply_markup=markup_iniciativa())
        for jogador in callback_mestre.listaJogadores:
            enviarMensagem(jogador, f'A INICIATIVA ESTÁ FORMADA, ENVIEM SUAS APOSTAS: \n{txt}')
    elif call.data == 'cb_inAllPlayers':
        callback_mestre.listaJogadores = playerHandler.getAllNames()
        bot.send_message(call.from_user.id, 'Todos os jogadores foram adicionados')

    #ADICIONANDO APOSTAS
    elif call.data[-6:] == 'aposta':
        print('aaaaaa')
        callback_mestre.nome = str(call.data[:7]) 
        msg = bot.send_message(call.from_user.id, f'Quantas apostas deseja dar para {callback_mestre.nome}')
        bot.register_next_step_handler(msg, modificarAposta)

    else: return ContinueHandling()
    #else: return ContinueHandling()

#------------------------
#    Funções de mestre  
#------------------------

def resetHandler(message):
    try:
        resetHandler.listaJogadores = message.text.split('')
    except:
        resetHandler.listaJogadores = [message.text]
    bot.send_message(message.chat.id, 'Quais atributos mudar?', reply_markup=reset_markup())
def givePH(message):
    print(callback_mestre.listaJogadores)
    quantia = int(message.text)
    playerHandler.give(callback_mestre.listaJogadores, 'ph', quantia)
    bot.send_message(message.chat.id, 'Jogadores atualizados', reply_markup=markup_mestre())
    for player in callback_mestre.listaJogadores:
        enviarMensagem(player, f"O mestre te deu {quantia} PH⭐️!")
def giveFortuna(message):
    print(callback_mestre.listaJogadores)
    quantia = int(message.text)
    playerHandler.give(callback_mestre.listaJogadores, 'fortuna', quantia)
    bot.send_message(message.chat.id, 'Jogadores atualizados', reply_markup=markup_mestre())
    for player in callback_mestre.listaJogadores:
        enviarMensagem(player, f"O mestre te deu {quantia} Fortuna💰!")
def registrarNPC(message):
    adicionarNPC(message.text)
    txt = apresentarIniciativa()
    bot.send_message(message.chat.id, f'NPC Adicionado: \n {txt}', reply_markup=markup_iniciativa())
def modificarAposta(message):
    quantidade = message.text
    print('===',quantidade, callback_mestre.nome)
    txt = adicionarAposta(callback_mestre.nome, quantidade)
    bot.send_message(message.chat.id, 'Apostas:\n'+txt, reply_markup=markup_iniciativa())

#||------------------------||
#||         Get ID         ||
#||------------------------||
@bot.message_handler(commands=['getID'])
def greet(message):
    bot.send_message(message.chat.id, message.chat.id)

#||------------------------||
#||    Calc de apostas     ||
#||------------------------||
@bot.message_handler(func=lambda message: True)
def rolagem(message):
    mensagem = message.text
    mensagem = mensagem.lower()
    mensagemCortada = mensagem.split(' ')
    operacao = mensagemCortada[0]

    if operacao == 'rolagem':
        print(tratarDados(mensagemCortada[1:], bot, message))
    else:
        try:
            operacao = int(operacao)
            dados, limite = tratarDados(mensagemCortada, bot, message)
            conjuntos, dadosRestantes = calcularConjuntos(dados, limite)
            tratarResposta(mensagemCortada, conjuntos, dadosRestantes, bot, message)
            print(str(message.chat.id)+'======')
            if message.chat.id == 5266515916: 
                mensagens = []
                mensagens = ['Te amo, xuxu', 'MANDA A BRAZA AMOR', 'ARROMBA O CU DESSES BRUTAMONTES', 'Te amo mtmtmt', '(≧ω≦)', 'Quer me foder com esse tanto de aposta? (╹◡╹)凸', 'Lembra de tomar agua ^^', 'Eita, olha q gatinha', '(adiciona mais uma aposta aí, mas n conta pra ngm 😈)', '(✿◠‿◠)ヽ(´▽｀)ノ', 'Espero que esteja se divertindo ^^', 'vc é foda (☞ﾟ∀ﾟ)☞', '＼（＾○＾）人（＾○＾）／ LET\'S GOOOOOOOOOOOOO', 'Te amo S2', 'Amo mtmtmt vc', 'Sheeeeesh, como vou prestar atenção no jogo com uma gatinha dessas na mesa?', '(figurinha dos gatos abraçando)', '∑(゜Д゜;) TUDO ISSO?!', '~(^з^)-', '(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧', 'Te amo mais q o Charlie', '(づ｡◕‿‿◕｡)づ', 'Sem mensagens, só beijinhos', 'Te amo tanto que todo fim de seção eu coloco umas mensagens extras, será que um dia vc vai ler todas?', 'Se você receber esta mensagem na seção, eu te devo uma salada do tasty (resgatável apenas com print)', 'Como vão os alfaces?', 'Te amo amor ^^']
                mensagens.append(f'Você sabia que existem {len(mensagens)+1} mensagens diferentes? será que já repetiu alguma?')
                print(f'mensagem personalizada de {len(mensagens)} mensagens')
                bot.send_message(message.chat.id, mensagens[randint(0, len(mensagens))])
        except: pass
    



bot.infinity_polling()


'''Fazer o treco de apostas,
   'Dar PH e Fortuna',
   Adicionar e Retirar Mestres
   Nome do PJ, editar nome do PJ
   INICIATIVA'''
'''☆'''
