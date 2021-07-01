#!/usr/bin/env python3

import time, argparse

from evdev import InputDevice, device, ecodes
from selectors import DefaultSelector, EVENT_READ

but = [307, 308, 305, 304, 315]

devices_list = list()
devices_dict= dict()

def set_devices(gp1, gp2):
	print(gp1, gp2)
	global devices_list, devices_dict
	devices_list = [gp1, gp2]
	devices_dict= {f'/dev/input/event{gp1}':'c' ,
				   f'/dev/input/event{gp2}':'c'}

gamepad1, gamepad2 = None, None
selector = DefaultSelector()

def bt_send_hat(path, que, val):
	# client.send_message('/bt', [int(path[-2:]), que, val])
	print(f'/bt, {int(path[-2:])}, {que}, {val}')
	global devices
	if val == 0: devices_dict[path] = 'c'
	else:        devices_dict[path] = que

def bt_send(path, que, val):
	# client.send_message('/bt', [int(path[-2:]), que, val])
	print(f'/bt, {int(path[-2:])}, {que}, {val}')

def input_bt():
	global gamepad1, gamepad2, devices_list, devices

	while True:
		# Si gamepad1 no está cargado, lo intenta cargar y registrarlo en selector
		if gamepad1 is None:
			try:
				gamepad1 = InputDevice(f'/dev/input/event{devices_list[0]}')
				selector.register(gamepad1, EVENT_READ)
				print('gamepad1 registred')
			except OSError as e: print(f'/dev/input/event{devices_list[0]} not connected')

		# Si gamepad2 no está cargado, lo intenta cargar y registrarlo en selector
		if gamepad2 is None:
			try:
				gamepad2 = InputDevice(f'/dev/input/event{devices_list[1]}')
				selector.register(gamepad2, EVENT_READ)
				print('gamepad2 registred')
			except OSError as e: print(f'/dev/input/event{devices_list[1]} not connected')

		# Si ninguno de los dos está cargado, vuelve a intentar conectarlos
		if gamepad1 is None and gamepad2 is None:
			print('Please, turn them on.')
			time.sleep(1)
			continue

		# Revisa la lista de selector, esperando que llegue algo
		for key, mask in selector.select():
			device = key.fileobj
			path   = key.fileobj.path
			
			# Intenta leer en device. Si salta error...
			try:
				for event in device.read():
					et, ec, ev = event.type, event.code, event.value
					if et == ecodes.EV_ABS:
						# Analogo
						if ec == 1: bt_send(path, 'h', -ev)
						if ec == 0: bt_send(path, 'v', -ev)
						if   ec == 16 and ev == -1: bt_send_hat(path, 't', 1)
						elif ec == 16 and ev ==  1: bt_send_hat(path, 'b', 1)
						elif ec == 17 and ev == -1: bt_send_hat(path, 'r', 1)
						elif ec == 17 and ev ==  1: bt_send_hat(path, 'l', 1)
						if   ec == 1  and ev ==  0: bt_send_hat(path, 'r', 0)
						if   ec == 1  and ev ==  0: bt_send_hat(path, 'l', 0)
						if   ec == 0  and ev ==  0: bt_send_hat(path, 't', 0)
						if   ec == 0  and ev ==  0: bt_send_hat(path, 'b', 0)
						
					if et == ecodes.EV_KEY:
						if   ec == but[0]: bt_send(path, 0, ev)
						elif ec == but[1]: bt_send(path, 1, ev)
						elif ec == but[2]: bt_send(path, 2, ev)
						elif ec == but[3]: bt_send(path, 3, ev)
						elif ec == but[4]: bt_send(path, 4, ev)
			
			# ... es porque el gamepad se apagó. Lo cierra y lo desregistra de selector
			except OSError as e:
				device.close()
				print('input_bt() - Except - A gamepad is turned off')
				
				if path[-2:] == '16':
					print('Did GAMEPAD1 turned off? Unregistering it...')
					if gamepad1 != None:
						selector.unregister(gamepad1)
						gamepad1 = None
				
				if path[-2:] == '20':
					print('Did GAMEPAD1 turned off? Unregistering it...')
					if gamepad2 != None:
						selector.unregister(gamepad2)
						gamepad2 = None

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--gp1', type=int, default=16,help='Gamepad 1')
	parser.add_argument('--gp2', type=int, default=20,help='Gamepad 1')
	args = parser.parse_args()
	
	set_devices(args.gp1, args.gp2)

	try:
		input_bt()
	except KeyboardInterrupt:
		print(' Bye')

