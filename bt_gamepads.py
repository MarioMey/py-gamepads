#!/usr/bin/env python3
""" py-gamepads
This code is for connecting two bluetooth gamepads.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Mario Mey"
__contact__ = "mariomey@gmail.com"
__credits__ = ["Sam, from Core Electronics"]
__date__ = "2021/07/08"
__deprecated__ = False
__license__ = "GPLv3"
__maintainer__ = "developer"
__status__ = "Production"
__version__ = "0.2"

import time, argparse, subprocess
try:
	from obs_api import client, consola, c2, c3, c, thread
except:
	from obs_api_no_obs import client, consola, c2, c3, c, thread
	import sys

from evdev import InputDevice, ecodes
from selectors import DefaultSelector, EVENT_READ

class Bt:
	def __init__(self):
		self.but = [307, 308, 305, 304, 315]
		self.gamepad1, self.gamepad2 = None, None
		self.selector = DefaultSelector()
		self.devices_list = list()
		self.devices_dict = dict()
		self.bt_on = True

	def bt_send_hat(self, path, que, val):
		client.send_message('/bt', [int(path[-2:]), que, val])
		c2(f'/bt, {int(path[-2:])}, {que}, {val}')
		if val == 0: self.devices_dict[path] = 'c'
		else:        self.devices_dict[path] = que

	def bt_send(self, path, que, val):
		client.send_message('/bt', [int(path[-2:]), que, val])
		c2(f'/bt, {int(path[-2:])}, {que}, {val}')

	def reconnect(self):
		device1 = '13:57:90:05:0E:31'
		device2 = '13:6E:0E:07:0E:31'
		ps1 = subprocess.Popen(['bluetoothctl', 'info', device1], stdout=subprocess.PIPE)
		ps2 = subprocess.Popen(['bluetoothctl', 'info', device2], stdout=subprocess.PIPE)
		stdout1 = subprocess.check_output(['grep', 'Connected'], stdin=ps1.stdout).decode("utf-8")
		stdout2 = subprocess.check_output(['grep', 'Connected'], stdin=ps2.stdout).decode("utf-8")
		if 'No' in stdout1 or 'no' in stdout1:
			subprocess.Popen(['bluetoothctl', 'connect', device1])
			c3(f'bluetoothctl connect {device1}')
		if 'No' in stdout2 or 'no' in stdout2:
			subprocess.Popen(['bluetoothctl', 'connect', device2])
			c3(f'bluetoothctl connect {device2}')

	def is_none(self, num, dev):
		gamepad = f'gamepad{num}'
		device = f'/dev/input/event{dev}'
		try:
			vars(self)[gamepad] = InputDevice(device)
			try:     self.selector.unregister(vars(self)[gamepad])
			except:  c3(f'Todavía no registrado {device}', c.azul)
			try:
				     self.selector.register(vars(self)[gamepad], EVENT_READ)
				     c3(f'Registrado {device}', c.cian)
			except:  c3(f'{device} already registred', c.cian)

		except OSError as e:
			c3(f'No está conectado {device}')

			# Probando device + 1
			dev += 1
			device = f'/dev/input/event{dev}'
			try:
				vars(self)[gamepad] = InputDevice(device)
				try:     self.selector.unregister(vars(self)[gamepad])
				except:  c3(f'Todavía no registrado {device}', c.azul)
				try:
						self.selector.register(vars(self)[gamepad], EVENT_READ)
						c3(f'Registrado {device}', c.cian)
				except:  c3(f'{device} already registred', c.cian)
			except OSError as e:
				c3(f'Ni tampoco...     {device}')

	def check_devices(self):
		while self.bt_on:
			# Si no están cargados, los intenta cargar y registrarlos en selector
			if self.gamepad1 is None:
				self.is_none(1, self.devices_list[0])
			if self.gamepad2 is None:
				self.is_none(2, self.devices_list[1])
			time.sleep(1)

	def input_bt(self, gp1, gp2):
		self.devices_list = [gp1, gp2]
		self.devices_dict= {f'/dev/input/event{gp1}':'c',
					        f'/dev/input/event{gp2}':'c'}
		
		client.send_message('/bt_init', [gp1, gp2])

		thread(self.check_devices)
		
		time.sleep(2)
		while self.bt_on:
			
			# Si ninguno de los dos está cargado, vuelve a intentar conectarlos
			if self.gamepad1 is None and self.gamepad2 is None:
				c3('No está conectado ninguno')
				time.sleep(1)
				continue

			# Revisa la lista de selector, esperando que llegue algo
			for key, mask in self.selector.select():
				device = key.fileobj
				path   = key.fileobj.path
				
				# Intenta leer en device. Si salta error...
				try:
					for event in device.read():
						et, ec, ev = event.type, event.code, event.value
						if et == ecodes.EV_ABS:
							# Analogo
							if ec == 1: self.bt_send(path, 'h', -ev)
							if ec == 0: self.bt_send(path, 'v', -ev)
							if   ec == 16 and ev == -1: self.bt_send_hat(path, 't', 1)
							elif ec == 16 and ev ==  1: self.bt_send_hat(path, 'b', 1)
							elif ec == 17 and ev == -1: self.bt_send_hat(path, 'r', 1)
							elif ec == 17 and ev ==  1: self.bt_send_hat(path, 'l', 1)
							if   ec == 1  and ev ==  0: self.bt_send_hat(path, 'r', 0)
							if   ec == 1  and ev ==  0: self.bt_send_hat(path, 'l', 0)
							if   ec == 0  and ev ==  0: self.bt_send_hat(path, 't', 0)
							if   ec == 0  and ev ==  0: self.bt_send_hat(path, 'b', 0)
							
						if et == ecodes.EV_KEY:
							if   ec == self.but[0]: self.bt_send(path, 0, ev)
							elif ec == self.but[1]: self.bt_send(path, 1, ev)
							elif ec == self.but[2]: self.bt_send(path, 2, ev)
							elif ec == self.but[3]: self.bt_send(path, 3, ev)
							elif ec == self.but[4]: self.bt_send(path, 4, ev)
				
				# ... es porque el gamepad se apagó. Lo cierra y lo desregistra de selector
				except OSError as e:
					device.close()
					c3('input_bt() - Except - Se apagó un gamepad')
					
					if path[-2:] == '16':
						c3(f'¿Se apagó /dev/input/event{self.devices_list[0]}? Desregistrándolo...')
						if self.gamepad1 != None:
							self.selector.unregister(self.gamepad1)
							self.gamepad1 = None
					
					if path[-2:] == '20':
						c3(f'¿Se apagó /dev/input/event{self.devices_list[1]}? Desregistrándolo...')
						if self.gamepad2 != None:
							self.selector.unregister(self.gamepad2)
							self.gamepad2 = None
			
			# c4('input_bt() Fin de WHILE')


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--gp1', type=int, default=16,help='Gamepad 1')
	parser.add_argument('--gp2', type=int, default=20,help='Gamepad 2')
	args = parser.parse_args()
	
	bt = Bt()

	try:
		consola(f'"R": reconnect()', c.naranja)
		consola(f'"Q": quit', c.naranja)

		thread(bt.input_bt, [args.gp1, args.gp2])

		while True:
			tecla = input()
			if tecla == 'r':
				bt.reconnect()
			elif tecla == 'q':
				sys.exit()
	except KeyboardInterrupt:
		print(' Bye')
