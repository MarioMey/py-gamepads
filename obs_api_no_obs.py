#!/usr/bin/env python3

import random, threading

from pythonosc import udp_client
targetIp = "127.0.0.1"
targetPort = 10000
client = udp_client.SimpleUDPClient(targetIp, targetPort)
client.send_message("/init", 1)

class Gd:
	def __init__(self) -> None:
		self.gd = {'verbose': [True, True, True, True]}

globalDict = Gd()

class Color:
	def __init__(self):
		self.reset = '\x1b[0m'
		self.blanco = '\x1b[97m'
		self.negro = '\x1b[90m'
		self.rojo = '\x1b[91m'
		self.verde = '\x1b[92m'
		self.azul = '\x1b[94m'
		self.amarillo = '\x1b[93m'
		self.magenta = '\x1b[95m'
		self.magenta_bold = '\x1b[95;1m'
		self.azul_bold = '\x1b[94;1m'
		self.cian = '\x1b[96m'
		self.naranja = '\x1b[38;5;202m'
		self.violeta = '\x1b[38;5;129m'
		self.rosa = '\x1b[38;5;213m'
		self.ocre = '\x1b[38;5;172m'
		self.marron = '\x1b[38;5;52m'
		self.musgo = '\x1b[38;5;58m'
		self.error = '\x1b[93;41m'
		self.remoto = '\x1b[93;42m'
		self.debug = '\x1b[93;44m'
		self.lista_attrs = []
		self.attrs = self.__dict__
		
		for k, v in self.attrs.items():
			if k not in ['lista_attrs', 'attrs', 'random']:
				self.lista_attrs.append(v)
	
		self.random = random.choice(self.lista_attrs)
c = Color()

# Threading
def thread(function, args=[]):
	t = threading.Thread(
		target=function,
		args=(args),
		name=f'{function}({args})',
		daemon=True)
	t.start()

def c1(texto, color_texto=c.azul_bold):
	if globalDict.gd['verbose'][0]:
		texto = str(texto)
		print(color_texto, texto, c.reset)

def c2(texto, color_texto=c.azul):
	if globalDict.gd['verbose'][1]:
		texto = str(texto)
		print(color_texto, texto, c.reset)

def c3(texto, color_texto=c.cian):
	if globalDict.gd['verbose'][2]:
		texto = str(texto)
		print(color_texto, texto, c.reset)

def c4(texto, color_texto=c.rosa):
	if globalDict.gd['verbose'][3]:
		texto = str(texto)
		print(color_texto, texto, c.reset)

def consola(texto, color_texto=c.verde):
	texto = str(texto)
	print(color_texto, texto, c.reset)