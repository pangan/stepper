from lib import WebServer
import sys
import datetime 
import signal

def myhandler(signum, frame):
	webif.close()
	exit(1)

def time_stamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def send_command(cmd):
	f = open('/tmp/m_command.txt','w')
	f.write(cmd)
	f.close()
	

def getweb():

  try:
  	data_dic = webif.read()
  except Exception:
  	exit(1)
    
  if data_dic:

    if 'c' in data_dic:
      if data_dic['c'] == 'forward':
        print >>sys.stderr, '[%s] FORWARD   ' %time_stamp(), webif.client
        send_command("FORWARD")
        
      if data_dic['c'] == 'reverce':
        print >>sys.stderr, '[%s] REVERCE   ' %time_stamp(), webif.client
        send_command("REVERCE")
        
      if data_dic['c'] == 'right':
        print >>sys.stderr, '[%s] RIGHT     ' %time_stamp(), webif.client
        send_command("RIGHT")
        
      if data_dic['c'] == 'left':
        print >>sys.stderr, '[%s] LEFT      ' %time_stamp(), webif.client
        send_command("LEFT")
        
      if data_dic['c'] == 'startstop':
        print >>sys.stderr, '[%s] START/STOP' %time_stamp(), webif.client
        send_command("STARTSTOP")
        
    if 'x' in data_dic:
      print >>sys.stderr, '[%s] EXIT' %time_stamp(), webif.client
      webif.close()
      
signal.signal(signal.SIGINT, myhandler)

webif = WebServer(port=8080,template='template.html')
print "Press Ctrl+c to exit!"
while True:
	getweb()