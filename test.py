import signal,os

def myhandler(signum, frame):
	print "signal %s %s" %(signum, frame)
	#exit(1)


signal.signal(signal.SIGINT, myhandler)
while True:
	os.kill(os.getpid(), signal.SIGINT)
