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
__version__ = "0.3"

import json, time, argparse
try:
	from obs_api import client, consola, c2, c3, c4, c, thread
except:
	from obs_api_no_obs import client, consola, c2, c3, c4, c, thread
	import sys

from evdev import InputDevice, ecodes
from selectors import DefaultSelector, EVENT_READ

class Bt:
	def __init__(self):
		self.buttons = [307, 308, 305, 304, 315, 310, 311, 312, 313]
		self.selector = DefaultSelector()
		self.devices = dict()
		self.bt_on = True

	def bt_send_hat(self, dev, path, que, val):
		client.send_message('/bt', [dev, que, val])
		c2(f'/bt, {dev}, {path[-2:]}, {que}, {val}')
		for k,v in self.devices.items():
			if v['path'] == path: dev = k
		if val == 0: self.devices[dev]['hat'] = 'c'
		else:        self.devices[dev]['hat'] = que
	
	def bt_send(self, dev, path, que, val):
		client.send_message('/bt', [dev, que, val])
		c2(f'/bt, {dev}, {path[-2:]}, {que}, {val}')

	def connect(self, num):

		for dev in range(15, 30):

			if dev in [val['event'] for val in self.devices.values()]:
				c4(f'dev {dev} ya está en la lista')
				continue

			try:
				self.devices[num]['InputDevice'] = InputDevice(f'/dev/input/event{dev}')
				self.selector.register(self.devices[num]['InputDevice'], EVENT_READ)
				self.devices[num]['path'] = f'/dev/input/event{dev}'
				self.devices[num]['event'] = dev
				self.devices[num]['uniq'] = self.devices[num]['InputDevice'].uniq
				self.devices[num]['phys'] = self.devices[num]['InputDevice'].phys
				
				c3(f'Registrado /dev/input/event{dev}', c.debug)
				client.send_message(f'bt_init{num}', dev)
				time.sleep(1)
				break

			except OSError as e:
				c4(f'No ha nada conectado a /dev/input/event{dev}')
				pass

	def check_devices(self):
		
		while self.bt_on:
			for num, val in self.devices.items():
				if val['InputDevice'] == None:
					self.connect(num)
			# break
			time.sleep(1)

	def input_bt(self, cantidad):#, gp1, gp2):
		c4(f'input_bt()', c.violeta)

		for num in range(cantidad):
			self.devices[num] = {
				'InputDevice': None,
				'event': None,
				'path': '',
				'hat': 'c',
				'uniq':None,
				'phys':None
				}
		
		thread(self.check_devices)
		
		while self.bt_on:
			
			# Si ninguno de los dos está cargado, ni se fija
			if all(item == None for item in [val for val in self.devices.values()]):
				c3('No está conectado ninguno')
				time.sleep(1)
				continue

			# Revisa la lista de selector, esperando que llegue algo
			for key, mask in self.selector.select():
				device = key.fileobj
				path   = key.fileobj.path
				for k,v in self.devices.items():
					if v['path'] == path:
						dev = k

				# Intenta leer en device.
				try:
					self.read_device(dev, path, device)

				# Si salta error es porque el gamepad se apagó.
				except:
					event = int(path[-2:])
					for k, v in self.devices.items():
						if v['event'] == event: num = k

					c3(f'¿Se apagó gamepad{num} {path}? Desregistrándolo...', c.error)
					self.selector.unregister(self.devices[num]['InputDevice'])
					device.close()
					self.devices[num] = {
						'event': None,
						'path': '',
						'hat': 'c',
						'InputDevice': None,
						'uniq':None,
						'phys':None
						}

	def read_device(self, dev, path, device):

		for event in device.read():
			et, ec, ev = event.type, event.code, event.value
			if et == ecodes.EV_ABS:
				# Analogo
				if ec == 1:                 self.bt_send(    dev, path, 'h', -ev)
				if ec == 0:                 self.bt_send(    dev, path, 'v', -ev)
				if   ec == 16 and ev == -1: self.bt_send_hat(dev, path, 't', 1)
				elif ec == 16 and ev ==  1: self.bt_send_hat(dev, path, 'b', 1)
				elif ec == 17 and ev == -1: self.bt_send_hat(dev, path, 'r', 1)
				elif ec == 17 and ev ==  1: self.bt_send_hat(dev, path, 'l', 1)
				if   ec == 1  and ev ==  0: self.bt_send_hat(dev, path, 'r', 0)
				if   ec == 1  and ev ==  0: self.bt_send_hat(dev, path, 'l', 0)
				if   ec == 0  and ev ==  0: self.bt_send_hat(dev, path, 't', 0)
				if   ec == 0  and ev ==  0: self.bt_send_hat(dev, path, 'b', 0)
				
			if et == ecodes.EV_KEY:
				if   ec == self.buttons[0]: self.bt_send(dev, path,   0, ev)
				elif ec == self.buttons[1]: self.bt_send(dev, path,   1, ev)
				elif ec == self.buttons[2]: self.bt_send(dev, path,   2, ev)
				elif ec == self.buttons[3]: self.bt_send(dev, path,   3, ev)
				elif ec == self.buttons[4]: self.bt_send(dev, path,   4, ev)
				elif ec == self.buttons[5]: self.bt_send(dev, path,   5, ev)
				elif ec == self.buttons[6]: self.bt_send(dev, path,   6, ev)
				elif ec == self.buttons[7]: self.bt_send(dev, path,   7, ev)
				elif ec == self.buttons[8]: self.bt_send(dev, path,   8, ev)
				
def write_file():
	while True:
		with open("/home/mario/meytv/obs-scripts/write_file.watch", "w") as outfile:
			new_dict = {}
			for k,v in bt.devices.items():
				new_dict[k] = {
					# 'InputDevice': None,
					'event': v['event'],
					'path':  v['path'],
					'hat':   v['hat'],
					'uniq':  v['uniq'],
					'phys':  v['phys']
					}
			json.dump(new_dict, outfile, default=str, sort_keys=True, indent=2, ensure_ascii=False)
		time.sleep(0.25) # 16fps

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--c', type=int, default=2,help='Cantidad')
	args = parser.parse_args()

	try:
		consola(f'"R": reconnect()', c.naranja)
		consola(f'"Q": quit', c.naranja)

		bt = Bt()
		thread(bt.input_bt, [args.c])
		thread(write_file)

		while True:
			tecla = input()

			# Quit	
			if tecla == 'q':
				sys.exit()

			# Test
			elif tecla == 't':
				consola(f'bt.devices {bt.devices}')

	except KeyboardInterrupt:
		print(' Bye')
