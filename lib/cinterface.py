class CInterface(object):

	def __init__(self):
		self.infile = '/tmp/m_command.txt'

	def send_command(self, cmd):
		f = open(self.infile,'w')
		f.write(cmd)
		f.close()