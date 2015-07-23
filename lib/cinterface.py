import os.path

class CInterface(object):

	def __init__(self):
		self.infile = '/tmp/m_command.txt'

	def send_command(self, cmd):
		f = open(self.infile,'w')
		f.write(cmd)
		f.close()

	def read_command(self):
		if os.path.isfile(self.infile):
			try:
				f = open(self.infile,'r')
				cc = f.read().strip()
				f.close()
				os.remove(self.infile)
				return cc
			except Exception:
				return None
		else:
			return None