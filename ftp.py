import socket, getpass, select


def main():
	while True:
		#print('ftp>', end='')
		command = input('ftp> ')
		if command != '':
			process_command(command.split())


def process_command(input):
	try:
		COMMANDS[input[0]](input[1:])
	except KeyError:
		print('invalid command')


def connect(addr):
	with socket.create_connection((addr[0], 21)) as conn:
		#print('login for {}'.format(addr), end='')
		login = input('login for {}'.format(addr[0]))
		conn.send('USER {}\r\n'.format(login).encode())
		#print('password for {}'.format(login), end='')
		#password = input('password for {}'.format(login))
		password = getpass.getpass()


def close_connection(conn):


def read_answer(conn):
	r, _, _ = select.select(conn, None, None, 2)
	answ = b''
	while r:
		line = r.recv(1024)
		print(line.decode())
		answ += line


COMMANDS = {'open': connect}


if __name__ == '__main__':
	main()
