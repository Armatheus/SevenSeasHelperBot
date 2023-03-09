import os
from dotenv import load_dotenv
import telebot
from generalFunctions import *
from random import randint
from dataBaseFunctions import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.handler_backends import ContinueHandling

load_dotenv()

API_KEY = os.getenv('API_KEY_SEVENSEAS')
bot = telebot.TeleBot(API_KEY)
#bot.edit_message_text(chat_id=CHAT_WITH_MESSAGE, text=NEW_TEXT, message_id=MESSAGE_TO_EDIT)

#||------------------------||
#||         Markup         ||
#||------------------------||
def ficha_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Adicionar PH", callback_data="cb_ph"),
               InlineKeyboardButton('Adicionar Fortuna', callback_data='cb_fortuna'),
               InlineKeyboardButton("Adicionar Aposta", callback_data="cb_aposta"),
               InlineKeyboardButton("Ordem de Iniciativa", callback_data="cb_iniciativa"),
               InlineKeyboardButton("Ficha", callback_data="cb_ficha")
               )
    return markup
def ficha_markup_mestre():
    pass
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Resetar PJs', callback_data='cb_reset'),
               InlineKeyboardButton("Dar PH e Fortuna", callback_data="cb_give"),
               InlineKeyboardButton('Jogadores', callback_data="cb_jogadores")
               )
    return markup
def reset_markup():
    pass
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Pontos Heróicos', callback_data='cb_resetPH'),
               InlineKeyboardButton('Fortuna', callback_data="cb_resetFortuna"),
               InlineKeyboardButton('Tudo', callback_data="cb_resetAll")
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
def tecladoNum_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    for i in range(3):
        markup.add(
        InlineKeyboardButton(((i*3)+1), callback_data=f'num_{(i*3)+1}'),
        InlineKeyboardButton(((i*3)+2), callback_data=f'num_{(i*3)+2}'),
        InlineKeyboardButton(((i*3)+3), callback_data=f'num_{(i*3)+3}'),
        )
    markup.add(
    InlineKeyboardButton('Apagar', callback_data='num_apagar'),
    InlineKeyboardButton('0', callback_data='num_0'),
    InlineKeyboardButton('Fim', callback_data='num_fim'),
    InlineKeyboardButton('Cancelar', callback_data='num_cancelar'),
    )
    return markup

#Handlers & Funções Gerais
imageHandler = ImageDataBase()
playerHandler = Jogador()

def enviarForce(nome, text):
    playerID = playerHandler.getPlayerID(nome)
    bot.send_message(playerID, text)

#||------------------------||
#||         HELP           ||
#||------------------------||
@bot.message_handler(commands=['help'])
def greet(message): 

    bot.reply_to(message, '''
A única função deste Bot, até o momento, é agrupar as suas apostas. 

Para isso, <b>mande um conjunto de números separados por um espaço</b>, ex: "1 1 9 8 7". <i>Números negativos viram positivos, e letras são desconsideradas</i>.

O <b>limite padrão é 10</b>, mas se quiser mudar <b>coloque um "/X" na mensagem</b>, <i>por exemplo: "5 5 5 /15"</i>.

Caso queira <b>adicionar um bônus em todos os dados</b> rolados coloque um <b>"*X"</b> na mensagem, <i>por exemplo: "1 3 5 4 10 *2" -> "3 5 7 6 12"</i>.

<i>A ordem dos fatores não altera o produto, mas o primeiro número não pode conter letras, "/" ou "*" </i>
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
            bot.send_message(message.chat.id, "renomeado com sucesso")
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


@bot.message_handler(commands=['getID'])
def greet(message):
    bot.send_message(message.chat.id, message.chat.id)

#||------------------------||
#||      ÁREA DA FICHA     ||
#||------------------------||
@bot.message_handler(commands=['f'])
def wellcome(message):
    pass
    jogadores = playerHandler.getFichasCriadas()
    if message.chat.id in jogadores: 
        bot.send_message(message.chat.id, 'Bem-vinda/Bem-vindo à area de ficha do bot! O que deseja fazer?', reply_markup=ficha_markup())
    else:
        playerHandler.criarFicha(message)
        bot.send_message(message.chat.id, 'Sua ficha foi criada, e agora?', reply_markup=ficha_markup())

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
        bot.send_message(call.from_user.id, ficha, 'HTML', reply_markup=ficha_markup())
    elif call.data == 'cb_ph':
        msg = bot.send_message(call.from_user.id, 'Quantos pontos quer adicionar? (números negativos são aceitos)')
        bot.register_next_step_handler(msg, atualizarPH)
        pass
    elif call.data == 'cb_fortuna':
        msg = bot.send_message(call.from_user.id, 'Quantos pontos quer adicionar? (números negativos são aceitos)')
        bot.register_next_step_handler(msg, atualizarFortuna)
        pass
    elif call.data == 'cb_aposta' or call.data == 'cb_iniciativa': bot.send_message(call.from_user.id, '''Função ainda não disponível 
┐(‘～`；)┌''', reply_markup=ficha_markup())

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
        

        pass
        
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
    return bot.send_message(message.from_user.id, f'<b>Pontos Heroicos:</b> {data[0]} → {data[1]}', 'HTML', reply_markup=ficha_markup())
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
    return bot.send_message(message.from_user.id, f'<b>Fortuna:</b> {data[0]} → {data[1]}', 'HTML', reply_markup=ficha_markup())
    
#||------------------------||
#||     ÁREA DO MESTRE     ||
#||------------------------||
@bot.message_handler(commands=['m'])
def wellcome(message):
    if  message.chat.id in playerHandler.mestreID:
        bot.send_message(message.chat.id, 'Qual o comando?', reply_markup=ficha_markup_mestre())
    else:
        bot.send_message(message.chat.id, '''Você não tem permissão para acessar os comandos de mestre
┐(‘～`；)┌''')

#------------------------
#    CALL BACK MANAGER
#------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_mestre(call):
    if call.data == 'cb_reset':
        callback_mestre.listaJogadores = []
        bot.send_message(call.from_user.id, 'Quais jogadores deseja resetar? ("all" para todos)', reply_markup=player_list_markup())
        #bot.register_next_step_handler(msg, resetHandler)
    elif  call.data == 'cb_give':
        pass
        callback_mestre.listaJogadores = []
        
    elif  call.data == 'cb_jogadores':pass
    else: return ContinueHandling()

#------------------------
#    Funções de mestre  
#------------------------

def resetHandler(message):
    
    if message.text == 'all':
        resetHandler.listaJogadores = playerHandler.getAllNames()
    else:
        try:
            resetHandler.listaJogadores = message.text.split('')
        except:
            resetHandler.listaJogadores = [message.text]
    bot.send_message(message.chat.id, 'Quais atributos mudar?', reply_markup=reset_markup())

#------
#  subcallhandler
#------
@bot.callback_query_handler(func=lambda call: True)
def callback_reset(call):
    ##SELECIONANDO ATRIBUTO DO RESET
    if call.data == 'cb_resetPH':
        print('LISTAJOGADORES:',callback_mestre.listaJogadores)
        txt = playerHandler.resetPJ('ph', callback_mestre.listaJogadores)
        bot.send_message(call.from_user.id, txt, 'HTML', reply_markup=ficha_markup_mestre())
    elif call.data == 'cb_resetAll': 
        print('LISTAJOGADORES:',callback_mestre.listaJogadores)
        txt = playerHandler.resetPJ('all', callback_mestre.listaJogadores)
        bot.send_message(call.from_user.id, txt, 'HTML', reply_markup=ficha_markup_mestre())
    elif call.data == 'cb_resetFortuna': 
        print('LISTAJOGADORES:',callback_mestre.listaJogadores)
        txt = playerHandler.resetPJ('fortuna', callback_mestre.listaJogadores)
        bot.send_message(call.from_user.id, txt, 'HTML', reply_markup=ficha_markup_mestre())
    
    ##SELECIONANDO JOGADORES DO RESET
    elif call.data in playerHandler.getAllNames():
        callback_mestre.listaJogadores.append(call.data)
        bot.send_message(call.from_user.id, call.data+' adicionado')
    elif call.data == 'cb_all':
        callback_mestre.listaJogadores = playerHandler.getAllNames()
        bot.send_message(call.from_user.id, 'Quais atributos mudar?', reply_markup=reset_markup())
    elif call.data == 'cb_fim':
        bot.send_message(call.from_user.id, 'Quais atributos mudar?', reply_markup=reset_markup())

    else: return ContinueHandling()


#||------------------------||
#||    CALC DE APOSTAS     ||
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
            if message.from_user.id == 5266515916:
                mensagens = ["Te amo, xuxu", "MANDA A BRAZA AMOR", "ARROMBA O CU DESSES BRUTAMONTES", "Te amo mtmtmt", "(≧ω≦)", "Quer me foder com esse tanto de aposta? (╹◡╹)凸", "Lembra de tomar agua ^^", "Eita, olha q gatinha", "(adiciona mais uma aposta aí, mas n conta pra ngm 😈)", "(✿◠‿◠)ヽ(´▽｀)ノ", "Espero que esteja se divertindo ^^", "vc é foda (☞ﾟ∀ﾟ)☞", "＼（＾○＾）人（＾○＾）／ LET'S GOOOOOOOOOOOOO", "Te amo S2", "Amo mtmtmt vc", "Sheeeeesh, como vou prestar atenção no jogo com uma gatinha dessas na mesa?", "(figurinha dos gatos abraçando)", "∑(゜Д゜;) TUDO ISSO?!", "~(^з^)-", "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", "Te amo mais q o Charlie", "(づ｡◕‿‿◕｡)づ", f"Você sabia? existem {len(mensagens)} diferentes, será que já repetiu alguma?", "Sem mensagens, só beijinhos", "Te amo tanto que todo fim de seção eu coloco umas mensagens extras, será que um dia vc vai ler todas?", "Se você receber esta mensagem na seção, eu te devo uma salada do tasty (resgatável apenas com print)", 'Como vão os alfaces?', 'Te amo amor ^^']
            bot.send_message(message.chat.id, mensagens[randint(0, len(mensagens))])
        except: pass
    



bot.infinity_polling()



'''Fazer o treco de apostas,
   'Jogadores' e 'Dar PH e Fortuna',
   Adicionar e Retirar Mestres
   Nome do PJ, editar nome do PJ'''
'''☆'''
