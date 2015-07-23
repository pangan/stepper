'''
Controlling motor by keyboard
2015-07-15
By Amir Mofakhar <pangan@gmail.com>
'''
import tty, termios
import threading
import sys
from lib import CInterface

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


threading.Thread(target = getchar).start()

ci = CInterface()

print "Press x to exit!"
global read_key
read_key = None

while True:

	if read_key == 'x':
		exit(1)
  	elif read_key in [chr(65),'w']:
  	   	''' UP '''
  	   	print "UP"
  	   	ci.send_command("FORWARD")
  	   	read_key = ''
  	elif read_key in [chr(66),'s']:
  		''' Down '''
  		print "DOWN"
  		ci.send_command("REVERCE")
  		read_key = ''
  	elif read_key in [chr(67),'d']:
  		''' Right '''
  		print "RIGHT"
  		ci.send_command("RIGHT")
  		read_key = ''
  	elif read_key in [chr(68),'a']:
  		''' Left '''
  		print "LEFT"
  		ci.send_command("LEFT") 
  		read_key = '' 
  	elif read_key == chr(13):
  		'''Start/Stop'''
  		ci.send_command("STARTSTOP")
  		print "START / STOP"
  		read_key = ''