import random
import logging
import sys, time
from lib import Daemon
from lib import CInterface
import os.path
import RPi.GPIO as GPIO


def init_log(log_file):
	logging.basicConfig(filename='/var/log/%s'%(log_file),level=logging.INFO,
	 format="[%(asctime)s][%(levelname)s] %(message)s",
	 datefmt="%Y-%m-%d %H:%M:%S")

class MyDaemon(Daemon):
	

	def run(self):

		
		GPIO.setmode(GPIO.BCM)

		# Define GPIO signals to use
		# Physical pins 11,15,16,18
		# GPIO17,GPIO22,GPIO23,GPIO24
		#if sys.argv[2]=='l':
		#StepPins = [4,17,27,22]
		#else:
		motors = [[18,23,24,25],[4,17,27,22]]

		# Set all pins as output
		for StepPins in motors:
		  for pin in StepPins:
		    GPIO.setup(pin,GPIO.OUT)
		    GPIO.output(pin, False)

		# Define advanced sequence
		# as shown in manufacturers datasheet

		Seq = [[1,0,0,0],
		       [1,1,0,0],
		       [0,1,0,0],
		       [0,1,1,0],
		       [0,0,1,0],
		       [0,0,1,1],
		       [0,0,0,1],
		       [1,0,0,1]
		       
		]
		

		StepCount = [len(Seq)-1, len(Seq)-1]
		#if sys.argv[3]=='b':
		#	StepDir = -1 # Set to 1 or 2 for clockwise
		            # Set to -1 or -2 for anti-clockwise
		#else:
		global StepDir

		StepDir= [1,1]

		# Read wait time from command line
		'''
		if len(sys.argv)>1:
		  WaitTime = int(sys.argv[1])/float(1000)
		else:
		  WaitTime = 1/float(1000)

		# Initialise variables
		'''
		StepCounter = [0,0]




		# Start main loop
		
		global START
		START = False
		







		
		m_command = None
		
		
		while True:

			m_command = ci.read_command()
			
			if m_command == 'FORWARD':
				logging.info("forward .....")
				StepDir = [1,1]

			elif m_command == 'REVERCE':
				logging.info("reverce .....")
				StepDir = [-1,-1]
			elif m_command == 'RIGHT':
				logging.info("right .....")
				StepDir = [1,-1]
			elif m_command == 'LEFT':
				logging.info("left .....")
				StepDir = [-1,1]
			elif m_command == 'STARTSTOP':
				logging.info("startstop .....")
				if START:
					START = False
					GPIO.cleanup()
				else:
					START = True
					GPIO.setmode(GPIO.BCM)
					for StepPins in motors:
						for pin in StepPins:
							GPIO.setup(pin,GPIO.OUT)
							GPIO.output(pin, False)

			
			if START:
				i = 0
				
				for StepPins in motors:
					if i == 0:
						i = 1
					else: i = 0

					for pin in range(0, 4):
						xpin = StepPins[pin]
						if Seq[StepCounter[i]][pin]!=0:
							#print " Step %i Enable %i" %(StepCounter,xpin)
							GPIO.output(xpin, True)
						else:
							GPIO.output(xpin, False)

				for i in range(0,2):

					StepCounter[i] += StepDir[i]
					if (StepCounter[i]>=StepCount[i]):
						StepCounter[i] = 0
					if (StepCounter[i]<0):
						StepCounter[i] = StepCount[i]

				time.sleep(0.001)
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



