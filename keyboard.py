'''
Controlling motor by keyboard
2015-07-15
By Amir Mofakhar <pangan@gmail.com>
'''
import tty, termios
import threading
import sys


def getchar():
  #Returns a single character from standard input
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
    tty.setraw(sys.stdin.fileno())
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  
  if ch:
    global read_key
    read_key = ch
    
  if ch !='x':
    #print ord(ch)
    threading.Thread(target = getchar).start()

def send_command(cmd):
	f = open('/tmp/m_command.txt','w')
	f.write(cmd)
	f.close()


threading.Thread(target = getchar).start()

print "Press x to exit!"
global read_key
read_key = None

while True:

	if read_key == 'x':
		exit(1)
  	elif read_key in [chr(65),'w']:
  	   	''' UP '''
  	   	print "UP"
  	   	send_command("FORWARD")
  	   	read_key = ''
  	elif read_key in [chr(66),'s']:
  		''' Down '''
  		print "DOWN"
  		send_command("REVERCE")
  		read_key = ''
  	elif read_key in [chr(67),'d']:
  		''' Right '''
  		print "RIGHT"
  		send_command("RIGHT")
  		read_key = ''
  	elif read_key in [chr(68),'a']:
  		''' Left '''
  		print "LEFT"
  		send_command("LEFT") 
  		read_key = '' 
  	elif read_key == chr(13):
  		'''Start/Stop'''
  		send_command("STARTSTOP")
  		print "START / STOP"
  		read_key = ''