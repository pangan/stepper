import random
import logging
import sys, time
from lib import Daemon
from lib import CInterface
import os.path



def init_log(log_file):
	logging.basicConfig(filename='/var/log/%s'%(log_file),level=logging.INFO,
	 format="[%(asctime)s][%(levelname)s] %(message)s",
	 datefmt="%Y-%m-%d %H:%M:%S")

class MyDaemon(Daemon):
	

	def run(self):
		m_command = None
		while True:
			m_command = ci.read_command()
			
			if m_command == 'FORWARD':
				logging.info("forward .....")
			elif m_command == 'REVERCE':
				logging.info("reverce .....")
			elif m_command == 'RIGHT':
				logging.info("right .....")
			elif m_command == 'LEFT':
				logging.info("left .....")
			elif m_command == 'STARTSTOP':
				logging.info("startstop .....")

			#time.sleep(3)
			#logging.info("-> %s" %m_command)


ci = CInterface()

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



