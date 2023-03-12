from tinydb import TinyDB, Query
from tinydb.operations import *
from dataBaseFunctions import Jogador
#import random

turnosdb = TinyDB('TurnosDb')
turno = Query()

def abrirIniciativa(jogadores):
    finalizarIniciativa()
    
    for jogador in jogadores:
        turnosdb.insert({'nome': jogador, 'apostas': 0})
    
    return apresentarIniciativa()

def finalizarIniciativa():
    turnosdb.truncate()

def apresentarIniciativa():
    iniciativa = computarIniciativa()
    iniciativaString = ''
    for jogador in iniciativa:
        print(jogador['apostas'], jogador['nome'])
        iniciativaString = iniciativaString + f'\n{jogador["apostas"]} {jogador["nome"]}'

    return iniciativaString

def computarIniciativa():
    iniciativa = []
    for jogador in turnosdb:
        iniciativa.append(jogador)

    iniciativa = sorted(iniciativa, key=lambda jogador: jogador['apostas'], reverse=True)
    return iniciativa


def adicionarAposta(nome, quantidade):
    personagem = turnosdb.search(turno.nome == nome)
    turnosdb.update({'apostas': (personagem[0]['apostas']+int(quantidade))}, turno.nome == nome) 

    return apresentarIniciativa()

def adicionarApostaId(id, quantidade):
    playerHandler = Jogador()
    ficha = playerHandler.getFicha(id)
    nome = ficha['rg']['jogadorNome']    


    personagem = turnosdb.search(turno.nome == nome)
    turnosdb.update({'apostas': (personagem[0]['apostas']+int(quantidade))}, turno.nome == nome) 

    return apresentarIniciativa()


def adicionarNPC(nome):
    turnosdb.insert({'nome': nome, 'apostas': 0})











