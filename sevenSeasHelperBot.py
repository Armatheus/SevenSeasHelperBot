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
    markup.add(InlineKeyboardButton('Adicionar PH β­οΈ', callback_data='cb_ph'),
               InlineKeyboardButton('Adicionar Fortuna π°', callback_data='cb_fortuna'),
               InlineKeyboardButton('Adicionar Aposta π₯', callback_data='cb_aposta'),
               InlineKeyboardButton('Ordem de Iniciativaπ', callback_data='cb_iniciativa'),
               InlineKeyboardButton('Ficha π°', callback_data='cb_ficha')
               )
    return markup
def markup_mestre():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Resetar PJs β»οΈ', callback_data='cb_reset'),
               InlineKeyboardButton('Dar PH e Fortuna π', callback_data='cb_give'),
               InlineKeyboardButton('Iniciativa π', callback_data='cb_markupIniciativa'),
               InlineKeyboardButton('Jogadores π΄ββ οΈ', callback_data='cb_jogadores'),
               )
    return markup
def markup_iniciativa():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Nova Iniciativa β»οΈ', callback_data='cb_iniciarIniciativa'),
               InlineKeyboardButton('Adicionar NPC π΄ββ οΈ', callback_data='cb_adicionarNPC'),
               InlineKeyboardButton('Adicionar Apostas π₯', callback_data='cb_apostasMestre'),
               InlineKeyboardButton('Ver Iniciativa π', callback_data='cb_iniciativaMestre'),
               InlineKeyboardButton('Voltar π', callback_data='cb_voltar'),
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
    markup.add(InlineKeyboardButton('Pontos HerΓ³icos β­οΈ', callback_data='cb_resetPH'),
               InlineKeyboardButton('Fortuna π°', callback_data='cb_resetFortuna'),
               InlineKeyboardButton('Tudo', callback_data='cb_resetAll')
               )
    return markup
def give_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('PH β­οΈ', callback_data='cb_givePH'),
               InlineKeyboardButton('Fortuna π°', callback_data='cb_giveFortuna')
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
#Handlers & FunΓ§Γ΅es Gerais
imageHandler = ImageDataBase()
playerHandler = Jogador()

#||------------------------||
#||       FunΓ§Γ΅es          ||
#||------------------------||
def enviarMensagem(nome, texto):
    playerID = playerHandler.getPlayerID(nome)
    bot.send_message(playerID, texto, parse_mode='HTML')

#||------------------------||
#||         HELP           ||
#||------------------------||
@bot.message_handler(commands=['help'])
def greet(message): 

    bot.reply_to(message, '''
FunΓ§Γ΅es do bot:
<b>βAgrupar dados em apostasβ</b>

-Mande um conjunto de nΓΊmeros <u>separados por um espaΓ§o</u>, 
<i>ex: "1 1 9 8 7". NΓΊmeros negativos viram positivos, e letras sΓ£o desconsideradas</i>.
-Se quiser <u>mudar o limite</u> coloque um <u>"/X"</u> na mensagem, 
<i>ex: "5 5 5 /15", o limite padrΓ£o Γ© 10</i>.
-Caso queira <u>adicionar um bΓ΄nus</u> em todos os dados rolados, coloque um <u>"*X"</u> na mensagem, <i>por exemplo: "1 3 5 4 10 *2" -> "3 5 7 6 12"</i>.
<i>A ordem dos fatores nΓ£o altera o produto, <b>mas o primeiro nΓΊmero nΓ£o pode conter letras, "/" ou "*"</b> </i>


<b>βControlar sua Fichaβ</b>

mande um "/f" no chat, Γ© bem intuitivo.
    ''', parse_mode='HTML')

#||------------------------||
#||    ΓREA DE IMAGENS     ||
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
                except: bot.send_message(message.chat.id, 'mas a imagem Γ© incompativel, delete ela antes de continuar')
            elif not resultado:
                bot.send_message(message.chat.id, 'essa imagem jΓ‘ existe')
        except:
            bot.send_message(message.chat.id, 'ERROR 001, verifique se colocou "tag url"')
    elif operacao == 'deletar':
        try:
            resultado = imageHandler.deletarImagem(mensagem[2])
            if resultado:
                bot.send_message(message.chat.id, 'imagem deletada >:3')
            elif not resultado:
                bot.send_message(message.chat.id, 'imagem nΓ£o encontrada')
        except:
            bot.send_message(message.chat.id, 'ERROR 002')
    elif operacao == 'catalogo'or operacao=='galeria':
        try:
            listas = imageHandler.catalogo()
            bot.send_message(message.chat.id, 'seu catΓ‘logo:')
            for i in range(len(listas[0])):
                try:
                    bot.send_photo(message.chat.id, 'https://docs.google.com/uc?id='+listas[1][i], caption=f'{listas[0][i]}')
                except:
                    bot.send_message(message.chat.id, f'a imagem {listas[0][i]} nΓ£o pode ser carregada.')
        except: bot.send_message(message.chat.id, 'ERROR 005')
    elif operacao == 'help':
        try:
            bot.send_message(message.chat.id, '''
    O comando de imagem Γ© apenas para o mestre, por favor nΓ£o mude nada, as mudanΓ§as sΓ£o feitas num database, entΓ£o Γ© irreversΓ­vel

    <b>nova (ou adicionar):</b> tag, url cortada 
    <b>deletar:</b> tag
    <b>catalogo(ou galeria):</b> nada
    <b>renomear:</b> tag, nova tag
        ''', 'HTML')
        except: bot.send_message(message.chat.id, 'ERROR 006, mermΓ£o, o help deu error, fodeu')
    elif operacao == 'renomear':
        '''try:'''
        rename = imageHandler.renomearTag(mensagem[2], mensagem[3])
        if rename:
            bot.send_message(message.chat.id, 'renomeado com sucesso')
        elif not rename:
            bot.send_message(message.chat.id, 'nΓ£o foi possΓ­vel mudar a tag')
        '''except:
            bot.send_message(message.chat.id, 'ERROR 003')'''
    else: 
        try:
            find = imageHandler.encontrarImagem(mensagem[1])
            if not find:
                bot.send_message(message.chat.id, 'imagem nΓ£o encontrada')
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
        msg = bot.send_message(call.from_user.id, 'Quantos pontos quer adicionar? (nΓΊmeros negativos sΓ£o aceitos)')
        bot.register_next_step_handler(msg, atualizarPH)
    elif call.data == 'cb_fortuna':
        msg = bot.send_message(call.from_user.id, 'Quantos pontos quer adicionar? (nΓΊmeros negativos sΓ£o aceitos)')
        bot.register_next_step_handler(msg, atualizarFortuna)
    elif call.data == 'cb_aposta': 
        msg = bot.send_message(call.from_user.id, 'Quantos pontos adicionar?')
        bot.register_next_step_handler(msg, modificarApostaJogador)
    elif call.data ==  'cb_iniciativa':
        txt = apresentarIniciativa()
        bot.send_message(call.from_user.id, f'Iniciativa: \n{txt}', reply_markup=markup_jogador())

    else: return ContinueHandling()

#------------------------
#    FunΓ§Γ΅es de ficha  
#------------------------

def atualizarPH(message):
    quantia = message.text
    try: quantia = int(quantia)
    except:
        quantia.lower()
        if quantia != 'cancelar': 
            msg = bot.send_message(message.from_user.id, 'Por favor, envie um nΓΊmero inteiro, envie "cancelar" para cancelar a operaΓ§Γ£o')
            bot.register_next_step_handler(msg, atualizarPH)
        return
    data = playerHandler.adicionarPH(message.from_user.id, quantia)
    return bot.send_message(message.from_user.id, f'<b>Pontos Heroicos:</b> {data[0]} β {data[1]}', 'HTML', reply_markup=markup_jogador())
def atualizarFortuna(message):
    quantia = message.text
    try: quantia = int(quantia)
    except:
        quantia.lower()
        if quantia != 'cancelar': 
            msg = bot.send_message(message.from_user.id, 'Por favor, envie um nΓΊmero inteiro, envie "cancelar" para cancelar a operaΓ§Γ£o')
            bot.register_next_step_handler(msg, atualizarFortuna)
        return
    data = playerHandler.adicionarFortuna(message.from_user.id, quantia)
    return bot.send_message(message.from_user.id, f'<b>Fortuna:</b> {data[0]} β {data[1]}', 'HTML', reply_markup=markup_jogador())
def modificarApostaJogador(message):
    txt = adicionarApostaId(message.from_user.id, message.text)
    bot.send_message(message.from_user.id, f'Iniciativa:\n {txt}', reply_markup=markup_jogador())
#||------------------------||
#||      ΓREA DA FICHA     ||
#||------------------------||
@bot.message_handler(commands=['f'])
def wellcome(message):
    jogadores = playerHandler.getFichasCriadas()
    if message.chat.id in jogadores: 
        bot.send_message(message.chat.id, 'Bem-vinda/Bem-vindo Γ  area de ficha do bot! O que deseja fazer?', reply_markup=markup_jogador())
    else:
        playerHandler.criarFicha(message)
        bot.send_message(message.chat.id, 'Sua ficha foi criada, e agora?', reply_markup=markup_jogador())

#||------------------------||
#||     ΓREA DO MESTRE     ||
#||------------------------||
@bot.message_handler(commands=['m'])
def wellcome(message):
    if  message.chat.id in playerHandler.mestreID:
        bot.send_message(message.chat.id, 'Qual o comando?', reply_markup=markup_mestre())
    else:
        bot.send_message(message.chat.id, '''VocΓͺ nΓ£o tem permissΓ£o para acessar os comandos de mestre
β(βο½`οΌ)β''')

#------------------------
#    CALL BACK MANAGER
#------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_mestre(call):
    print(computarIniciativa())

    if call.data == 'cb_reset':
        callback_mestre.listaJogadores = []
        bot.send_message(call.from_user.id, 'Quais jogadores deseja resetar?', reply_markup=player_list_markup())
        #bot.register_next_step_handler(msg, resetHandler)
    elif  call.data == 'cb_give':
        callback_mestre.listaJogadores = []   
        bot.send_message(call.from_user.id, 'Para quais jogadores deseja dar?', reply_markup=player_givelist_markup())
    elif  call.data == 'cb_jogadores':
        message = playerHandler.consultarJogadores(call)
        bot.send_message(call.from_user.id, message, 'HTML', reply_markup=markup_mestre())
    elif call.data == 'cb_iniciarIniciativa':
        callback_mestre.listaJogadores = [] 
        bot.send_message(call.from_user.id, 'Quais jogadores estarΓ£o na cena?', reply_markup=player_inlist_markup())
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
        jogadores = playerHandler.getAllNames()
        for jogador in jogadores:
            enviarMensagem(jogador, f'')
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
        msg = bot.send_message(call.from_user.id, 'Quantos pontos quer adicionar? (nΓΊmeros negativos sΓ£o aceitos)')
        bot.register_next_step_handler(msg, givePH)
    elif call.data == 'cb_giveFortuna':
        msg = bot.send_message(call.from_user.id, 'Quantos pontos quer adicionar? (nΓΊmeros negativos sΓ£o aceitos)')
        bot.register_next_step_handler(msg, giveFortuna)
    
    #CRIANDO UMA NOVA INICIATIVA
    elif call.data == 'cb_inFim':
        #bot.send_message(call.from_user.id, 'Qual atributo mudar?', reply_markup=give_markup())
        txt = abrirIniciativa(callback_mestre.listaJogadores)
        bot.send_message(call.from_user.id, f'Jogadores em cena: \n{txt}', reply_markup=markup_iniciativa())
        for jogador in callback_mestre.listaJogadores:
            print(jogador)
            enviarMensagem(jogador, f'A INICIATIVA ESTΓ FORMADA, ENVIEM SUAS APOSTAS: \n{txt}')
    elif call.data == 'cb_inAllPlayers':
        callback_mestre.listaJogadores = playerHandler.getAllNames()
        bot.send_message(call.from_user.id, 'Todos os jogadores foram adicionados')

    #ADICIONANDO APOSTAS
    elif call.data[-6:] == 'aposta':
        print('aaaaaa')
        print(call.data[-6:])
        print(str(call.data[:-7]))
        callback_mestre.nome = str(call.data[:-7]) 
        msg = bot.send_message(call.from_user.id, f'Quantas apostas deseja dar para {callback_mestre.nome}')
        bot.register_next_step_handler(msg, modificarAposta)

    else: return ContinueHandling()
    #else: return ContinueHandling()

#------------------------
#    FunΓ§Γ΅es de mestre  
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
        enviarMensagem(player, f"O mestre te deu {quantia} PHβ­οΈ!")
def giveFortuna(message):
    print(callback_mestre.listaJogadores)
    quantia = int(message.text)
    playerHandler.give(callback_mestre.listaJogadores, 'fortuna', quantia)
    bot.send_message(message.chat.id, 'Jogadores atualizados', reply_markup=markup_mestre())
    for player in callback_mestre.listaJogadores:
        enviarMensagem(player, f"O mestre te deu {quantia} Fortunaπ°!")
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
                mensagens = ['Te amo, xuxu', 'MANDA A BRAZA AMOR', 'ARROMBA O CU DESSES BRUTAMONTES', 'Te amo mtmtmt', '(β§Οβ¦)', 'Quer me foder com esse tanto de aposta? (βΉβ‘βΉ)εΈ', 'Lembra de tomar agua ^^', 'Eita, olha q gatinha', '(adiciona mais uma aposta aΓ­, mas n conta pra ngm π)', '(βΏβ βΏβ )γ½(Β΄β½ο½)γ', 'Espero que esteja se divertindo ^^', 'vc Γ© foda (βοΎβοΎ)β', 'οΌΌοΌοΌΎβοΌΎοΌδΊΊοΌοΌΎβοΌΎοΌοΌ LET\'S GOOOOOOOOOOOOO', 'Te amo S2', 'Amo mtmtmt vc', 'Sheeeeesh, como vou prestar atenΓ§Γ£o no jogo com uma gatinha dessas na mesa?', '(figurinha dos gatos abraΓ§ando)', 'β(γΠγ;) TUDO ISSO?!', '~(^Π·^)-', '(οΎβγ?β)οΎ*:ο½₯οΎβ§', 'Te amo mais q o Charlie', '(γ₯ο½‘ββΏβΏβο½‘)γ₯', 'Sem mensagens, sΓ³ beijinhos', 'Te amo tanto que todo fim de seΓ§Γ£o eu coloco umas mensagens extras, serΓ‘ que um dia vc vai ler todas?', 'Se vocΓͺ receber esta mensagem na seΓ§Γ£o, eu te devo uma salada do tasty (resgatΓ‘vel apenas com print)', 'Como vΓ£o os alfaces?', 'Te amo amor ^^']
                mensagens.append(f'VocΓͺ sabia que existem {len(mensagens)+1} mensagens diferentes? serΓ‘ que jΓ‘ repetiu alguma?')
                print(f'mensagem personalizada de {len(mensagens)} mensagens')
                bot.send_message(message.chat.id, mensagens[randint(0, len(mensagens))])
        except: pass
    



bot.infinity_polling()


'''Fazer o treco de apostas,
   'Dar PH e Fortuna',
   Adicionar e Retirar Mestres
   Nome do PJ, editar nome do PJ
   INICIATIVA'''
'''β'''
