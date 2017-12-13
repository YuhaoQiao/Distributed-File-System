import sys, socket, struct, random

class Client():

	#List of valid commands
	commands = ["READ FILE", "WRITE FILE", "PWDIR", "CHDIR", "LS", "QUIT"]

	def __init__(self, port):

		s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s1.settimeout(1.5)
		self.ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
		self.port = port
		s1.connect(("0.0.0.0", self.port))

		valid = False

		while 1:

			while not valid:
				self.message = raw_input(">: ")
				if any(x in self.message for x in self.commands):
					valid = True
				else:
					print "Invalid Command\n"
			s1.sendall(self.message)
			if self.message == "QUIT":
				sys.exit()
			try:
				recv_data = s1.recv(4096)
				print recv_data + '\n'
				valid = False;
			except socket.timeout:
				print "Something went wrong\n"


if __name__ == '__main__':

	port = int(sys.argv[1])
	Client(port)
