import socket, getpass, select, re


CONNECTION = None


def main():
	while True:
		#print('ftp>', end='')
		command = input('ftp> ')
		if command != '':
			process_command(command.split())


def process_command(args):
	try:
		COMMANDS[args[0]](args[1:])
	except KeyError:
		print('invalid command')


def connect(addr):
	global CONNECTION
	if CONNECTION is not None:
		print('Connection is open already')
		return
	if len(addr) != 1:
		print('incorrect number of arguments, expected 1, but was {}'.format(len(addr)))
	CONNECTION = socket.create_connection((addr[0], 21))
	#CONNECTION.settimeout(2)
	print(read_answer(), end='')
	#print('login for {}'.format(addr), end='')
	login = input('login for {} '.format(addr[0]))
	CONNECTION.send('USER {}\r\n'.format(login).encode())
	print(read_answer(), end='')
	print('password for {} '.format(login), end='')
	password = input('password for {} '.format(login))
	#password = getpass.getpass('Password: ')
	CONNECTION.send('PASS {}\r\n'.format(password).encode())
	print(read_answer(), end='')


def close_connection(args):
	if len(args) > 0:
		print('incorrect number of arguments, expected 0, but was {}'.format(len(args)))
	if CONNECTION is None:
		print('connection is not open')
		return
	CONNECTION.close()
	print('connection closed')


def read_answer():
	r, _, _ = select.select([CONNECTION], [], [], 2)
	answ = b''
	if r:
		line = r[0].recv(1024)
		#print(line.decode())
		answ += line
	return answ.decode()
	# result = []
	# s = CONNECTION.makefile()
	# answ = s.readline()
	# while re.match('\d{3} ', answ) == None:
	# 	#answ = CONNECTION.recv(1024)
	#
	# 	# if not answ:
	# 	# 	break
	# 	result.append(answ)
	# 	answ = s.readline()
	# result.append(answ)
	# return ''.join(result)


COMMANDS = {'open': connect, 'close': close_connection}


if __name__ == '__main__':
	main()
