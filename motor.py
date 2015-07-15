import random
import logging
import sys, time
from lib import Daemon
import os.path



def init_log(log_file):
	logging.basicConfig(filename='/var/log/%s'%(log_file),level=logging.INFO,
	 format="[%(asctime)s][%(levelname)s] %(message)s",
	 datefmt="%Y-%m-%d %H:%M:%S")

class MyDaemon(Daemon):
	
	def read_command(self,cfile):

		if os.path.isfile(cfile):
			try:
				f = open(cfile,'r')
				cc = f.read()
				f.close()
				os.remove(cfile)
				return cc
			except Exception:
				logging.warning("NO File!")
				return None
		else:
			return None

	def run(self):
		m_command = None
		while True:
			file_command = self.read_command('/tmp/m_command.txt')
			if file_command:
				m_command = file_command

			time.sleep(3)
			logging.info("-> %s" %m_command)



init_log('%s.log' %sys.argv[0])

if __name__ == "__main__":
	daemon = MyDaemon('/tmp/%s.pid'% sys.argv[0])

	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			logging.info("starting service")
			try:
				daemon.start()
			except Exception, e:
				logging.error('Shutting down ! %s' %e)

		elif 'stop' == sys.argv[1]:
			logging.info("stopping service")
			try:
				daemon.stop()
			except Exception, e:
				logging.error('Could not stop! %s' %e)

		elif 'restart' == sys.argv[1]:
			logging.info("restarting service")
			try:
				daemon.restart()
			except Exception, e:
				logging.error('Could not restart! %s' %e)

		elif 'status' == sys.argv[1]:
			pid = daemon.status()
			if pid:
				print "Service is running [pid:%s]" %pid
			else:
				print "Service is stopped!"
		else:
			print "Unknown command!"
			sys.exit(2)

		sys.exit(0)
	else:
		print "usage: %s start|stop|restart|status" % sys.argv[0]
		sys.exit(2)



