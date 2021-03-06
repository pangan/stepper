import sys
import time
import RPi.GPIO as GPIO
import tty, termios
import threading
import datetime 

from webinterface import WebServer

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


def time_stamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def getweb():

  
  data_dic = webif.read()
  
  read_web = None
  if data_dic:

    if 'c' in data_dic:
      if data_dic['c'] == 'forward':
        print >>sys.stderr, '[%s] FORWARD   ' %time_stamp(), webif.client
        read_web = 'w'
        
      if data_dic['c'] == 'reverce':
        print >>sys.stderr, '[%s] REVERCE   ' %time_stamp(), webif.client
        read_web = 's'
        
      if data_dic['c'] == 'right':
        print >>sys.stderr, '[%s] RIGHT     ' %time_stamp(), webif.client
        read_web = 'd'
        
      if data_dic['c'] == 'left':
        print >>sys.stderr, '[%s] LEFT      ' %time_stamp(), webif.client
        read_web = 'd'
        
      if data_dic['c'] == 'startstop':
        #print >>sys.stderr, '[%s] START/STOP' %time_stamp(), webif.client
        read_web = chr(13)
        

    if 'x' in data_dic:
      print >>sys.stderr, '[%s] EXIT' %time_stamp(), webif.client
      
      webif.close()
      read_web = 'x'
    else:
      if read_web:
        global read_key
        print "---->"
        read_key = read_web
      
    


def motor():
  
  global read_key
  global START
  global StepDir

  if read_key == 'x':
    GPIO.cleanup()
    exit(1)
  elif read_key in [chr(65),'w']:
    ''' UP '''
    StepDir = [1,1]
    read_key = ''
  elif read_key in [chr(66),'s']:
    ''' Down '''
    StepDir = [-1,-1]
    read_key = ''
  elif read_key in [chr(67),'d']:
    ''' Right '''
    StepDir = [1,-1]
    read_key = ''
  elif read_key in [chr(68),'a']:
    ''' Left ''' 
    StepDir = [-1,1]
    read_key = '' 

  elif read_key == chr(13):
    if START:
      START = False
    else:
      START = True
    read_key = ''


  if START:
    i = 0
    for StepPins in motors:
      if i == 0:
        i = 1
      else: i = 0
      for pin in range(0, 4):
        xpin = StepPins[pin]
        #print StepCounter
        #print pin
        if Seq[StepCounter[i]][pin]!=0:
          #print " Step %i Enable %i" %(StepCounter,xpin)
          GPIO.output(xpin, True)
        else:
          GPIO.output(xpin, False)

    for i in range(0,2):
      StepCounter[i] += StepDir[i]

      # If we reach the end of the sequence
      # start again
      if (StepCounter[i]>=StepCount[i]):
        StepCounter[i] = 0
      if (StepCounter[i]<0):
        StepCounter[i] = StepCount[i]

    # Wait before moving on
    time.sleep(WaitTime)

  threading.Thread(target = motor).start()
  


# Use BCM GPIO references
# instead of physical pin numbers
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
    print "Setup pins"
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
if len(sys.argv)>1:
  WaitTime = int(sys.argv[1])/float(1000)
else:
  WaitTime = 1/float(1000)

# Initialise variables
StepCounter = [0,0]




# Start main loop
global read_key
read_key = ''
global START
START = False

threading.Thread(target = getchar).start()
print "Press x to exit!"

#global webif
webif = WebServer(port=8080,template='template.html')

#threading.Thread(target = getweb).start()

threading.Thread(target = motor).start()


while True:
  
  
  getweb()

  