eracao = int(operacao)
        print('==')
        dados, limite = tratarDados(mensagemCortada, bot, message)
        print(message.from_user.id+'======')
        print('=======')
        conjuntos, dadosRestantes = calcularConjuntos(dados, limite)
        tratarResposta(mensagemCortada, conjuntos, dadosRestantes, bot, message)
        print('==')
        print(message.chat.id+'======')
        if message.chat.id == 5266515916:
            mensagens = ['Te amo, xuxu', 'MANDA A BRAZA AMOR', 'ARROMBA O CU DESSES BRUTAMONTES', 'Te amo mtmtmt', '(≧ω≦)', 'Quer me foder com esse tanto de aposta? (╹◡╹)凸', 'Lembra de tomar agua ^^', 'Eita, olha q gatinha', '(adiciona mais uma aposta aí, mas n conta pra ngm 😈)', '(✿◠‿◠)ヽ(´▽｀)ノ', 'Espero que esteja se divertindo ^^', 'vc é foda (☞ﾟ∀ﾟ)☞', '＼（＾○＾）人（＾○＾）／ LET\'S GOOOOOOOOOOOOO', 'Te amo S2', 'Amo mtmtmt vc', 'Sheeeeesh, como vou prestar atenção no jogo com uma gatinha dessas na mesa?', '(figurinha dos gatos abraçando)', '∑(゜Д゜;) TUDO ISSO?!', '~(^з^)-', '(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧', 'Te amo mais q o Charlie', '(づ｡◕‿‿◕｡)づ', f'Você sabia? existem {len(mensagens)} diferentes, será que já repetiu alguma?', 'Sem mensagens, só beijinhos', 'Te amo tanto que todo fim de seção eu coloco umas mensagens extras, será que um dia vc vai ler todas?', 'Se você receber esta mensagem na seção, eu te devo uma salada do tasty (resgatável apenas com print)', 'Como vão os alfaces?', 'Te amo amor ^^']
            bot.send_message(message.chat.id, mensagens[randint(0, len(mensagens))])